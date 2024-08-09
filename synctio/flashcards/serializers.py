from rest_framework import serializers
from .models import Flashcard, Deck, Folder, FlashcardImpression

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Flashcard
        fields='__all__'
class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model=Deck
        fields='__all__'
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Folder
        fields='__all__'
class FlashcardImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model=FlashcardImpression
        fields='__all__'