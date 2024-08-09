#check for unique email and username
from django.contrib.auth import get_user_model
from django import forms
import pytz
from django.forms import ModelForm

User=get_user_model()

def timezones():
    timezones=[]
    for x in pytz.common_timezones:
        timezones.append([x, x])
    return timezones

class changeUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user=kwargs.pop('user')
        super(changeUserForm,self).__init__(*args, **kwargs)
    email= forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
    #            "class":"form-control",
                "id":"user-email"
            }
        )
    )

    date_of_birth=forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(
            attrs={
 #               "class":"form-control",
                "id":"user-dob",
                "type":"date"
            }
        ),
    )
    goal=forms.ChoiceField(
        label="Studying Goal",
        choices=[
            ("05","5 min"),
            ("15","15 min"),
            ("30","30 min"),
            ("45","45 min"),
        ],
        widget=forms.RadioSelect(
            attrs={
 #               "class":"form-control",
                "id":"user-goal",
            }
        ),
    )
    timezone=forms.ChoiceField(
        label="Timezone",
        choices=timezones(),
        widget=forms.Select(
            attrs={
 #               "class":"form-control",
                "id":"user-timezone",
            }
        ),
    )
    profile=forms.ChoiceField(
        label="Profile Picture",
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
        widget=forms.RadioSelect(
            attrs={
                "id":"user-profile",
            },
        ),
    )
    def clean_username(self):
        username=self.cleaned_data.get("username")
        if self.user.username!=username:
            qs= User.objects.filter(username__iexact=username)
            if qs.exists():
                raise forms.ValidationError("This is an invalid username, please pick another.")
            return username
#    def clean_username(self):
 #       username=self.cleaned_data.get("username")
  #      qs= User.objects.filter(username__iexact=username)
   #     if qs.exists():
    #        raise forms.ValidationError("This is an invalid username, please pick another.")
     #   return username

class registerForm(forms.Form):
    username=forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
      #          "class":"input",
                "id":"user-username",
            }
        )
    )
    email= forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
         #       "class":"form-control",
                "id":"user-email"
            }
        )
    )
    password1=forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(
            attrs={
      #          "class":"form-control",
                "id":"user-password"
            }
        )
    )
    password2=forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
         #       "class":"form-control",
                "id":"user-confirm-password"
            }
        )
    )
    date_of_birth=forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={
  #              "class":"form-control",
                "id":"user-dob",
                "type":"date"

            }
        )
    )
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Your Password does not match")
    def clean_username(self):
        username=self.cleaned_data.get("username")
        qs= User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username

class LoginForm(forms.Form):
    username=forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
#                "class":"form-control",
                "id":"user-email"
            }
        )
    )
    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
 #               "class":"form-control",
                "id":"user-password"
            }
        )
    )
#    def clean(self):
#        username=self.cleaned_data.get("username")
#        password=self.cleaned_data.get("password")

    def clean_username(self):
        username=self.cleaned_data.get("username")
        qs= User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user")
        return username