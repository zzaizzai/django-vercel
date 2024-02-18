from django.db import models, connection
from core.common_funcs import dictfetchall


# Create your models here.
class Project(models.Model):
    name = models.CharField('project name', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, max_length=255)

    class Meta:
        managed = False  # Exclude this model from migrations
        db_table = 'project' 

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls):
        sql = """
        SELECT
        *
        FROM project
        """

        # Execute the SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql)
            
            row = dictfetchall(cursor)
        
        return row

    @classmethod
    def create_table(cls):
        # Drop existing table if it exists
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS project")

        # Create a new table
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls)

        return "Table created successfully"
    
    @classmethod
    def create_demo_data(cls):
        sql = """
        INSERT INTO project (name, created_at, description)
        VALUES
            ('Project 1', NOW(), 'Description for Project 1'),
            ('Project 2', NOW(), 'Description for Project 2'),
            ('Project 3', NOW(), 'Description for Project 3')
        """

        # Execute the SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql)

        return "Demo data created successfully"