from django.urls import path
from . import views


urlpatterns = [
    path('schedule/',views.schedule, name="schedule"),
    path('createTimestamp/',views.createTimestamp, name="createTimestamp"),
    path('stopTimestamp/',views.stopTimestamp, name="stopTimestamp"),
    path('startTimestamp/',views.startTimestamp, name="startTimestamp"),
    path('getTimestamp/',views.getTimestamp, name="getTimestamp"),

]

