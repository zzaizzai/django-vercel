from django.db import models, connection
from core.common_funcs import dictfetchall


# Create your models here.
class Projects(models.Model):
    title = models.CharField('project name', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, max_length=255)
    created_user_id = models.IntegerField() 
    created_user_name = models.CharField(max_length=100, null=True)
    
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
    
class DemoData():
    
    @classmethod
    def create_demo_data_projects(cls):
        Projects(title='Project 1', description = 'Description for Project 1', created_user_id= 1, created_user_name='User1 for Demo').create_a_project()
        Projects(title='Project 2', description = 'Description for Project 2', created_user_id= 1, created_user_name='User1 for Demo').create_a_project()
        Projects(title='Project 3', description = 'Description for Project 3', created_user_id= 1, created_user_name='User1 for Demo').create_a_project()
        
        
        
        