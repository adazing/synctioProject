from django.urls import path, re_path
from . import views

urlpatterns = [
    path('openaiapi/', views.check, name="openai"),
 #   path('processor/', views.processor, name="processor"),
    path('flashcard-processor/', views.flashcardfindapiview, name="flashcardProcessor"),
]