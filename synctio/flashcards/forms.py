from django.forms import ModelForm

from .models import Deck, Folder, Flashcard, FlashcardImpression
from django import forms

#class DeckIdForm(forms.Form):
 #   flashcard=forms.IntegerField(
  #      label="flashcard",
   #     widget=forms.TextInput(
    #        attrs={
     #           "id":"flashcardknowledge-flashcard",
      #      }
       # ),
    #)

class createFolderEmpty(ModelForm):
    previous_folder=forms.CharField(
        max_length=1000000,
        label="previous_folder",
        widget=forms.TextInput(
            attrs={
                "id":"previous_folder",
            }
        ),
    )
    class Meta:
        model = Folder
        fields = [
            "name",
            "description",
        ]

class createDeckEmpty(ModelForm):
    folder=forms.CharField(
        max_length=1000000,
        label="folder",
        widget=forms.TextInput(
            attrs={
                "id":"folder",
            }
        ),
    )
    class Meta:
        model = Deck
        fields = [
            "name",
            "description"
        ]
        

class findFlashcardForm(forms.Form):
    flashcard=forms.IntegerField(
        label="flashcard",
        widget=forms.TextInput(
            attrs={
                "id":"flashcardknowledge-flashcard",
            }
        ),
    )
    review=forms.ChoiceField(
        label="review",
        choices=[
            ("1","1"),
            ("0","0"),
            ("2","2"),
        ],
        widget=forms.RadioSelect(
            attrs={
 #               "class":"form-control",
                "id":"flashcardknowledge-review",
            }
        ),
    )

class FolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = [
            "previous_folder",
            "name",
            "description",
        ]



class FlashcardForm(ModelForm):
    class Meta:
        model=Flashcard
        fields=[
            "deck",
            "key",
            "answer",
        #    "image"
        ]

class DeckForm(ModelForm):
    class Meta:
        model = Deck
        fields = (
            "folder",
            "name",
            "description",
        )
    def __init__(self, *args, **kwargs):
  #      self.user=kwargs.pop('user')
        super(DeckForm, self).__init__(*args, **kwargs)
#        self.fields['folder'].queryset=Folder.objects.none()
   #     def clean(self):
    #        cleaned_data=super().clean()
     #       folder_id=cleaned_data.get('folder')
      #      cleaned_data['folder']=Folder.objects.get(id=folder_id)
