from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Timestamp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_on = models.BooleanField()
    seconds = models.IntegerField()