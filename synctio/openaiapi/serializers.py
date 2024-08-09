from rest_framework import serializers

class FlashcardInformation(serializers.Serializer):
    key = serializers.CharField(max_length=200)
    answer = serializers.CharField(max_length=200)
    id = serializers.IntegerField()