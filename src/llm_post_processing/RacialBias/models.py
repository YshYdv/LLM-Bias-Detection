from django.db import models

# Create your models here.

class inputData(models.Model):
    id = models.IntegerField(primary_key=True)
    input_data = models.TextField()
    prediction = models.IntegerField()