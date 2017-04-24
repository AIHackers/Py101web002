from django.db import models

# Create your models here.
class Data(models.Model):
    city = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    temperature = models.IntegerField()
    last_update = models.CharField(max_length=200)
