from django.db import models

# Create your models here.
class movieinfo (models.Model):
    title=models.CharField(max_length=250)
    year=models.IntegerField(null=True)
    description=models.TextField()