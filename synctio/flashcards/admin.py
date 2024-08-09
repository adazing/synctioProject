from django.contrib import admin

# Register your models here.
from .models import FlashcardImpression, Folder, Deck, Flashcard

# Register your models here.
admin.site.register(Folder)
admin.site.register(Deck)
admin.site.register(Flashcard)
admin.site.register(FlashcardImpression)