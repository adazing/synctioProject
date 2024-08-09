from django.shortcuts import render
from .models import Timestamp
from .forms import TimestampForm
# Create your views here.
from datetime import datetime, timedelta
from django.http import Http404, JsonResponse, HttpResponse
from django.utils import timezone
from accounts.models import Profile
from django.contrib.auth.decorators import login_required

@login_required
def getTimestamp(request):
    userProfile=Profile.objects.get(user=request.user)
    if userProfile.lastTimestamp!=None and userProfile.lastTimestamp.is_on==True:
        print(userProfile.lastTimestamp.end)
        print(userProfile.lastTimestamp.start)
        secLeft=(userProfile.lastTimestamp.end-timezone.now()).total_seconds()
        print(secLeft)
        print("hello")
        if secLeft>0:
            return JsonResponse({"on":True, "time":secLeft}, status=200)
        else:
            userProfile.lastTimestamp.is_on=False
            userProfile.lastTimestamp.save()
            userProfile.lastTimestamp=None
            userProfile.save()
            return JsonResponse({"on":False, "time":0}, status=200)
    elif userProfile.lastTimestamp!=None:
        if userProfile.lastTimestamp.seconds-(userProfile.lastTimestamp.start- userProfile.lastTimestamp.end).total_seconds()>0:
            return JsonResponse({"on":False, "time":userProfile.lastTimestamp.seconds-(userProfile.lastTimestamp.end-userProfile.lastTimestamp.start).total_seconds()})
        else:
            userProfile.lastTimestamp=None
            userProfile.save()
            return JsonResponse({"on":False, "time":0}, status=200)
    return JsonResponse({"on":False, "time":0}, status=200)

@login_required
def startTimestamp(request):#continues last timestamp by creating a new timestamp
    print("20")
    userProfile=Profile.objects.get(user=request.user)
    if userProfile.lastTimestamp!=None:
        secLeft=userProfile.lastTimestamp.seconds-(userProfile.lastTimestamp.end-userProfile.lastTimestamp.start).total_seconds()
     #   print("last profile sec: "+str(userProfile.lastTimestamp.seconds))
    #    print("lasttimestamp end: "+str(userProfile.lastTimestamp.end))
   #     print("lasttimestamp start: "+str(userProfile.lastTimestamp.start))
  #      print("difference: "+userProfile.lastTimestamp.seconds)
        timestamp=Timestamp.objects.create(user=request.user, start=timezone.now(), end=timezone.now()+timedelta(seconds=secLeft), is_on=True, seconds=secLeft)
        timestamp.save()
        userProfile=Profile.objects.get(user=request.user)
        userProfile.lastTimestamp=timestamp
        userProfile.save()
        return JsonResponse({"time":secLeft}, status=200)
    return JsonResponse({}, status=400)

@login_required
def stopTimestamp(request):#stops the current timestamp
    print("20")
    currentTimestamp=Timestamp.objects.filter(user=request.user).get(is_on=True)
    print(currentTimestamp)
    currentTimestamp.is_on=False
    currentTimestamp.end=timezone.now()
#    currentTimestamp.seconds=(currentTimestamp.end-currentTimestamp.start).total_seconds()
    currentTimestamp.save()
    #userProfile=Profile.objects.get(user=request.user)
    #userProfile.lastTimestamp=currentTimestamp
    #userProfile.save()
    # print(userProfile.lastTimestamp)
    return JsonResponse({}, status=200)

@login_required
def createTimestamp(request):#creates new timestamp
    form=TimestampForm(request.POST or None)#number of seconds
    print(form.errors)
    if form.is_valid():
        for x in Timestamp.objects.filter(user=request.user):
            if x.is_on:
                x.is_on=False
                x.end=timezone.now()
                x.save()
        sec=form.cleaned_data.get("seconds")
        timestamp=Timestamp.objects.create(user=request.user, start=timezone.now(), end=timezone.now()+timedelta(seconds=sec), is_on=True, seconds=sec)
        print("hi 18")
        timestamp.save()
        userProfile=Profile.objects.get(user=request.user)
        userProfile.lastTimestamp=timestamp
        userProfile.save()
        return JsonResponse({}, status=201)
    return JsonResponse({}, status=400)

@login_required
def schedule(request):
    return render(request, "schedule/pomodoroSchedule.html")
