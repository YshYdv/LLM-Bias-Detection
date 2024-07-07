from django.db import models

# Create your models here.

class InputData(models.Model):
    input_text = models.TextField()