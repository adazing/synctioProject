from django.contrib.auth import get_user_model
from django import forms
import pytz
from .models import Timestamp
from django.forms import ModelForm

class TimestampForm(forms.Form):
    seconds=forms.IntegerField()