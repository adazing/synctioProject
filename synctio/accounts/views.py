from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from .models import Profile
from flashcards.models import Flashcard, FlashcardImpression, Folder, Deck
from schedule.models import Timestamp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, registerForm,changeUserForm
#from axes.decorators import axes_dispatch
from django.db import transaction
from flashcards.models import Folder
from django.core.mail import send_mail
import datetime
from django.http import Http404, JsonResponse, HttpResponse
import pytz
from pytz import timezone
import pandas as pd
import datetime
from django.contrib.auth.decorators import login_required


def privacyPolicy(request):
    return render(request, 'accounts/privacy_policy.html')


def aboutUs(request):
    return render(request, 'accounts/aboutUs.html')

@login_required
def deleteTimeData(request):
    if request.method=="POST":
        timestamps=Timestamp.objects.filter(user=request.user)
        for x in timestamps:
            x.delete()
        return redirect("dashboard")
    return render(request,"accounts/delete.html", {'obj':'your time data'})

@login_required
def deleteFlashcardsData(request):
    if request.method=="POST":
        folders=Folder.objects.filter(user=request.user)
        for x in folders:
            x.delete()
        Folder.objects.create(previous_folder=None, user=request.user, name="Untitled", description=None)
        return redirect("dashboard")
    return render(request,"accounts/delete.html", {'obj':'your flashcards data (including folders, decks, and cards)'})


@login_required
def deleteUser(request):
    user= request.user
    if request.method=="POST":
        user.delete()
        return redirect("register")
    return render(request,"accounts/delete.html", {'obj':'your account'})

@login_required
def userOptions(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    form=changeUserForm(request.POST or None, initial={
        'email':user.email,
        'date_of_birth':profile.date_of_birth,
        'goal':profile.goal,
        'timezone':profile.timezone,
        'profile':profile.profilePicture,
        }, user=user)
    print(user)
    print("hi")
    if form.is_valid():
#        username=form.cleaned_data.get("username")
        email=form.cleaned_data.get("email")
        #don't print password or other sensitive data
        dob=form.cleaned_data.get("date_of_birth")
        goal=form.cleaned_data.get("goal")
        timezone=form.cleaned_data.get("timezone")
        profilePicture=form.cleaned_data.get("profile")
        print("email")
        print(email)
#        user.username=username
        user.email=email
        user.save()
        profile.date_of_birth=dob
        profile.goal=goal
        profile.timezone=timezone
        profile.profilePicture=profilePicture
        profile.save()
        print(user.email)
    return render(request, 'accounts/userOptions.html',{"form":form,'username':user.username})

@login_required
def dashboard(request):
    user=request.user
    profile=Profile.objects.get(user=request.user)
    print(Timestamp.objects.filter(user=request.user))
    day1=0
    day2=0
    day3=0
    day4=0
    day5=0
    for x in Timestamp.objects.filter(user=request.user):
        dif=(datetime.date.today()-x.start.date()).days        
        print(dif)
        if x.is_on==False:
            if dif>8 and x.is_on==False:
                x.delete()
            elif dif==0:
                day1+=(x.end-x.start).total_seconds()/60
            elif dif==1:
                day2+=(x.end-x.start).total_seconds()/60
            elif dif==2:
                day3+=(x.end-x.start).total_seconds()/60
            elif dif==3:
                day4+=(x.end-x.start).total_seconds()/60
            elif dif==4:
                day5+=(x.end-x.start).total_seconds()/60
    context={
        "user":user,
        "day1":day1,
        "day2":day2,
        "day3":day3,
        "day4":day4,
        "day5":day5,
        "goal":profile.goal,
        'profilePicture':profile.profilePicture
    }
    return render(request, 'accounts/dashboard.html',context)

# def updateTimePage(request):
#     current_date=datetime.datetime.now(datetime.timezone.utc).date()
# #    current_time=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
# #    current_date=datetime.datetime.now(datetime.timezone.utc).date()
# #    print(request.user)
#     profile=Profile.objects.get(user=request.user)
#     localtimezone=timezone(profile.timezone)
#     utc=timezone("UTC")
#     date=pd.to_datetime(profile.last_date)
#     diff=datetime.timedelta(minutes=(utc.localize(date)-localtimezone.localize(date).astimezone(utc)).seconds/3600)
#     lastdt=datetime.datetime.combine(date, datetime.datetime.min.time())
#     currentdt=datetime.datetime.combine(current_date, datetime.datetime.min.time())
#     if (currentdt-(lastdt-diff)).days==1:
#         profile.day5=profile.day4
#         profile.day4=profile.day3
#         profile.day3=profile.day2
#         profile.day2=profile.day1
#         profile.day1=0

#     elif (currentdt-(lastdt-diff)).days==2:
#         profile.day5=profile.day3
#         profile.day4=profile.day2
#         profile.day3=profile.day1
#         profile.day2=0
#         profile.day1=0

#     elif (currentdt-(lastdt-diff)).days==3:
#         profile.day5=profile.day2
#         profile.day4=profile.day1
#         profile.day3=0
#         profile.day2=0
#         profile.day1=0

#     elif (currentdt-(lastdt-diff)).days==4:
#         profile.day5=profile.day1
#         profile.day4=0
#         profile.day3=0
#         profile.day2=0
#         profile.day1=0

#     elif (currentdt-(lastdt-diff)).days>=4:
#         profile.day5=0
#         profile.day4=0
#         profile.day3=0
#         profile.day2=0
#         profile.day1=0

#     else:
#         profile.day1+=1#profile.day1+(current_time-profile.last_time).total_seconds()/60
#     #profile.last_time=current_time
#     #profile.last_date=current_date
#     profile.last_date=datetime.datetime.now(datetime.timezone.utc).date()
#     profile.save()
#     return JsonResponse({"response":(currentdt-(lastdt-diff)).days, "ex":profile.day1},status=201)


#@axes_dispatch
def registerPage(request):
    form=registerForm(request.POST or None)
    print(form.is_valid())
    print(form.errors)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        email=form.cleaned_data.get("email")
        password1=form.cleaned_data.get("password1")
        dob= form.cleaned_data.get("date_of_birth")
        try:
            with transaction.atomic():
                user=User.objects.create_user(username=username,email=email, password=password1)
                profile=Profile.objects.create(user=user, date_of_birth=dob)
     #           send_mail(
      #              "Welcome to Synctio",#subject
       #             "Hello, "+ user.name+"! This is the code to activate your account:",#message
        #            "adalangford123@gmail.com",#from email
         #           ["adalangford123@gmail.com"],#to email
          #      )
        except:
            user=None
        if user is not None:
            login(request, user)
            Folder.objects.create(previous_folder=None, user=request.user, name="Untitled", description=None)
            return redirect("/")
        else:
            request.session['register_error']=1
    return render(request, "accounts/login_register.html", {"form":form})

def loginPage(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        #don't print password or other sensitive data
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            request.session['invalid_user']=1
#    form=LoginForm()
    return render(request, "accounts/login_register.html", {"form":form})
 #   if request.method == "POST":
#        username= request.POST.get("username")
#        password= request.POST.get("password")
 #       try:
 #           user=User.objects.get(username=username)
  #      except:
  #          messages.error(request, "User does not exist")
    #context={}
  #  return render(request, 'accounts/login_register.html', context)

@login_required
def logoutPage(request):
    logout(request)
    return redirect('/login')

def homemain(request):
    return render(request, 'accounts/homemain.html')
