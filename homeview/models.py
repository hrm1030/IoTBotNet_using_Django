from django.db import models

# Create your models here.
class LogHistory(models.Model):  
    logid = models.CharField(max_length=20)  
    logname = models.CharField(max_length=100)  
    logdate = models.CharField(max_length=15) 
    logstate = models.CharField(max_length=15)  
    class Meta:  
        db_table = "loghistory"  

class User(models.Model):
    """Model definition for User."""

    # TODO: Define fields here
    id = models.IntegerField(max_length=255, primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    role = models.IntegerField(max_length=1)
    class Meta:
        """Meta definition for User."""

        db_table = "users"