from django.forms import ModelForm
from django import forms

class flashcardIdForm(forms.Form):
    flashcard=forms.IntegerField(
        label="flashcard",
        widget=forms.TextInput(
            attrs={
                "id":"answerForm-flashcard",
            }
        ),
    )

class answerForm(forms.Form):
    flashcardAnswer=forms.CharField(
        label="answer",
        widget=forms.TextInput(
            attrs={
                "id":"answerForm-flashcard-answer",
            }
        ),
    )
    answer=forms.CharField(
        label="answer",
        widget=forms.TextInput(
            attrs={
                "id":"answerForm-answer",
            }
        ),
    )
    flashcard=forms.IntegerField(
        label="flashcard",
        widget=forms.TextInput(
            attrs={
                "id":"answerForm-flashcard",
            }
        ),
    )
