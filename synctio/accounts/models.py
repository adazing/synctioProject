from django.db import models
from django.contrib.auth.models import User
import string
import random
import datetime
from django.utils import timezone
import pytz
from schedule.models import Timestamp

def timezones():
    timezones=[]
    for x in pytz.common_timezones:
        timezones.append([x, x])
    return timezones


def generate_unique_code():
    length=8
    code="".join(random.choices(string.ascii_uppercase, k=length))
    return code

# Create your models here.
class Profile(models.Model):
    code = models.CharField(max_length=10, default=generate_unique_code())                  #code for access
    user = models.OneToOneField(User, on_delete=models.CASCADE)                             #user
    date_of_birth = models.DateField()                                                      #date of birth
#    streak = models.IntegerField(default=0)                                                 #streak value
#    productivity_percentage=models.DecimalField(max_digits=5,decimal_places=2,default=0.00) #productivity percentage
#    last_date=models.DateField(auto_now_add=True)                                           #most recent day that user visited
#    level=models.IntegerField(default=0)                                                    #level of user
#    points=models.IntegerField(default=0)                                                   #points of user
#    day1=models.IntegerField(default=0)                                                     #day number 1 minutes active
#    day2=models.IntegerField(default=0)                                                     #day number 2 minutes active
#    day3=models.IntegerField(default=0)                                                     #day number 3 minutes active
#    day4=models.IntegerField(default=0)                                                     #day number 4 minutes active
#    day5=models.IntegerField(default=0)       
#    updated_time=models.DateTimeField(auto_now_add=True)
#    last_date=models.DateField(auto_now_add=True)                                           #most recent stored date
    #last_time=models.TimeField(auto_now_add=True)                                           #most recent stored date
    timezone=models.CharField(
        max_length=100,
        choices=timezones(),
        default="UTC",
    )
    goal=models.CharField(
        max_length=2,
        choices=[
            ("05","5 min"),
            ("15","15 min"),
            ("30","30 min"),
            ("45","45 min"),
        ],
        default="15",
    )
    lastTimestamp=models.ForeignKey(Timestamp, on_delete=models.SET_NULL,null=True, blank=True, default=None)
    profilePicture=models.CharField(
        max_length=2,
        choices=[
            ("1","1"),
            ("2","2"),
            ("3","3"),
            ("4","4"),
            ("5","5"),
            ("6","6"),
            ("7","7"),
            ("8","8"),
            ("9","9"),
            ("10","10"),
            ("11","11"),
            ("12","12"),
        ],
        default="1",
    )
