from django.db import models
from django.contrib.auth.models import User
import html.entities

# Create your models here.

class Folder(models.Model):
    previous_folder=models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class Deck(models.Model):
    folder =models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-updated', '-created']
    def __str__(self):
        return str(self.id)


class Flashcard(models.Model):
    deck=models.ForeignKey(Deck, on_delete=models.CASCADE)
    key= models.CharField(max_length=1000)
    answer=models.CharField(max_length=2000, null=True, blank=True)
 #   image=models.ImageField(upload_to="flashcards/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-created']
#    def __str__(self):
 #       return self.id

class FlashcardImpression(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="flashcardKnowledge_users")
    flashcard=models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name="flashcardKnowledge_flashcards")
    review=models.CharField(default="0",max_length=1)
    #levelknown = models.IntegerField(default=0)
    #leveltried = models.IntegerField(default=0)

  #  def __str__(self):
   #     return self.id
