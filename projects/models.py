from typing import List, Union
from django.db import models, connection
from core.common_funcs import dictfetchall
from datetime import date


class PostBaseModel(models.Model):
    title = models.CharField('title', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, max_length=255)
    
    created_user_id = models.IntegerField() 
    created_user_name = models.CharField(max_length=100, null=True)
    
    completed_at = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        
        
        
class Project(PostBaseModel, models.Model):
    
    def __str__(self):
        return self.title
    
    class Meta:
        managed = False  # Exclude this model from migrations
        db_table = 'projects' 

    @classmethod
    def get_all(cls, sort="desc"):

        sql_sort = "DESC"
        
        
        if sort == "asc":
            sql_sort = "asc"

        sql = f"""
        SELECT *
        FROM projects
        ORDER BY id {sql_sort}
        """

        # Execute the SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql)
            
            row = dictfetchall(cursor)
        
        return row
    
    @staticmethod
    def get_one_project(project_id: int) -> Union['Project', None]:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM projects where id = {project_id}")
            projects = dictfetchall(cursor)
            
            try:
                return Project(**projects[0])
            except Exception as e:
                return None

    
    def get_all_tasks(self) -> List['Task']:
        return Task.get_with_parent_id(self.id)
    
    def create_a_project(self):
        self.save()
        
    @classmethod
    def create_table(cls):
        # Drop existing table if it exists
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS projects")

        # Create a new table
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls)

        return "Table created successfully"


class Task(PostBaseModel, models.Model):

    parent_project_id = models.IntegerField()
    plan_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        managed = False  # Exclude this model from migrations
        db_table = 'tasks' 
    
    def create_a_task(self):
        self.save()
    
    def complete(self):
        self.is_completed = True
        self.completed_at = date.today()
        self.save()
    
    def uncomplete(self):
        self.is_completed = False
        self.completed_at = None
        self.save()
        
    @staticmethod
    def get_one_task_with_id(task_id: int) -> Union['Task', None]:
        return Task.objects.get(pk=task_id)
        
    @staticmethod
    def get_with_parent_id(parent_project_id: int) -> List['Task']:
        
        sort = 'ASC'
        
        sql = f"""
        SELECT *
        FROM tasks
        WHERE parent_project_id = {parent_project_id}
        ORDER BY plan_date {sort}
        """

        # Execute the SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql)
            
            tasks_dict = dictfetchall(cursor)
            
            tasks = [Task(**task) for task in tasks_dict]
            
        return tasks
    
    @staticmethod
    def delete_with_id(task_id: int) -> None:
        task = Task.objects.get(pk=task_id)
        task.delete()

    
    @classmethod
    def create_table(cls):
        # Drop existing table if it exists
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS tasks")

        # Create a new table
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls)

        return "Table created successfully"

    def create_a_task(self):
        self.save()
        
class DemoData():
    
    @classmethod
    def create_demo_data_projects(cls):
        Project(title='Project 1', description = 'Description for Project 1', created_user_id= 1, created_user_name='User1 for Demo').create_a_project()
        Project(title='Project 2', description = 'Description for Project 2', created_user_id= 1, created_user_name='User1 for Demo').create_a_project()
        Project(title='Project 3', description = 'Description for Project 3', created_user_id= 1, created_user_name='User1 for Demo').create_a_project()
        
        
        for i in range(1, 4):
            Task(title="Task 1" , description = 'Description for Task 1', created_user_id= 1, created_user_name='User1 for Demo', parent_project_id=i, plan_date = '2024-02-01').create_a_task()
            Task(title="Task 2" , description = 'Description for Task 2', created_user_id= 1, created_user_name='User1 for Demo', parent_project_id=i, plan_date = '2024-02-02').create_a_task()
            Task(title="Task 3" , description = 'Description for Task 3', created_user_id= 1, created_user_name='User1 for Demo', parent_project_id=i, plan_date = '2024-02-03').create_a_task()
        
        
        
        