from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('', views.homemain, name="homemain"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('user-options/', views.userOptions, name="userOptions"),
#    path('update-time-page/',views.updateTimePage, name="updateTime"),
    path('about-us/', views.aboutUs, name="aboutUs"),
    path('delete-user/', views.deleteUser, name="deleteUser"),
    path('delete-time-data/', views.deleteTimeData, name="deleteTimeData"),
    path('delete-flashcards-data/', views.deleteFlashcardsData, name="deleteFlashcardsData"),
    path('privacy-policy/', views.privacyPolicy, name="deleteFlashcardsData"),
]
