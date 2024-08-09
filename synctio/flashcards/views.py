from winreg import REG_OPTION_BACKUP_RESTORE
from xml.etree.ElementTree import TreeBuilder
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from .models import Folder, Deck, Flashcard, FlashcardImpression
from .forms import DeckForm, FolderForm, FlashcardForm, findFlashcardForm, createDeckEmpty, createFolderEmpty
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FlashcardSerializer, DeckSerializer, FolderSerializer, FlashcardImpressionSerializer
from django.views.generic import FormView
from rest_framework import generics
from rest_framework import status  # Import this for Status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response  # Import this for Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from synctio.settings import LOGIN_URL
from rest_framework import serializers
import random
from collections import OrderedDict

@login_required
def flashcardWordBlowing(request, pk):
    context={
        "deck":Deck.objects.get(id=pk).name
    }
    return render(request, "flashcards/windblowing.html", context)

@login_required
def flashcardCreateView(request):
    form=FlashcardForm(request.POST or None)
    if form.is_valid()==True:
        flashcard=Flashcard.objects.create(deck=form.cleaned_data.get("deck"), key=form.cleaned_data.get("key"), answer=form.cleaned_data.get("answer"))
        flashcard.save()
        return JsonResponse(FlashcardSerializer(flashcard).data, status=201)
    return JsonResponse({}, status=404)

@login_required
def folderCreateEmpty(request):
    form=createFolderEmpty(request.POST or None)
    if form.is_valid()==True:
        if form.cleaned_data.get("previous_folder")=="-1":
            folder=Folder.objects.create(previous_folder=None, user=request.user, name=form.cleaned_data.get("name"), description=form.cleaned_data.get("description"))
        else:
            folder=Folder.objects.create(previous_folder=Folder.objects.get(id=int(form.cleaned_data.get("previous_folder"))), user=request.user, name=form.cleaned_data.get("name"), description=form.cleaned_data.get("description"))
        folder.save()
 #       if folder.previous_folder==None:
 #           return JsonResponse({"previousfolderid":"-1", "foldername":folder.name, "folderid":str(folder.id)}, status=201)
 #       return JsonResponse({"previousfolderid":str(folder.previous_folder.id), "foldername":folder.name, "folderid":str(folder.id)}, status=201)
        return JsonResponse({}, status=201)
    return JsonResponse({}, status=404)

@login_required
def deckCreateEmpty(request):
    form=createDeckEmpty(request.POST or None)
    print(form.is_valid())
    print(form.errors)
    print(form.data)
    if form.is_valid()==True:
        print("form is valid")
        deck=Deck.objects.create(folder=Folder.objects.get(id=int(form.cleaned_data.get("folder"))), user=request.user, name=form.cleaned_data.get("name"), description=form.cleaned_data.get("description"))
        deck.save()
        for x in range(0, 3):
            Flashcard.objects.create(deck=deck, key="untitled", answer="untitled")
        return JsonResponse({"deckid":str(deck.id)}, status=201)
    return JsonResponse({}, status=404)

@login_required
def flashcardwriteview(request, pk):
    randomFlashcard=random.choice(Flashcard.objects.filter(deck=Deck.objects.get(id=pk)))
 #   print(FlashcardSerializer(randomFlashcard).data)
    context={
        "deck":Deck.objects.get(id=pk),
        "flashcard":FlashcardSerializer(randomFlashcard).data,
    }

    return render(request, "flashcards/flashcardwrite.html", context)

@login_required
def flashcardplayview(request, pk):
    randomFlashcard=random.choice(Flashcard.objects.filter(deck=Deck.objects.get(id=pk)))
 #   print(FlashcardSerializer(randomFlashcard).data)
    context={
        "deck":Deck.objects.get(id=pk),
        "flashcard":FlashcardSerializer(randomFlashcard).data,
    }

    return render(request, "flashcards/flashcardplay.html", context)


# class DeckApi(generics.ListAPIView):
#     queryset=Deck.objects.all()
#     serializer_class=DeckSerializer
#  #   def get_queryset(self):
#  #       return Deck.objects.filter(user=self.request.user)
# folders=Folder.objects.all()

# @api_view(['POST'])
# def FlashcardCreateView(request, pk):
#     serializer=FlashcardSerializer(data=request.POST or None)
#     if serializer.is_valid(raise_exception=True):
#         obj=serializer.save(deck=pk)
#         return Response(serializer.data)
#     return Response({}, status=400)

@login_required
def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ""
    if q!="":
        decks=Deck.objects.filter(user=request.user)
        decks = decks.filter(
            Q(folder__name=q) |
            Q(description__icontains=q)|
            Q(name__icontains=q)
            )
    else:
        decks=Deck.objects.filter(user=request.user)
    global foldersHTML
    foldersHTML=""
    folders=Folder.objects.filter(user=request.user)
    def recurseDict(parent_folder, counter):
        global foldersHTML
        if parent_folder==None:
           for f in folders.filter(previous_folder__isnull=True):
                foldersHTML+="<details id='folder-"+str(f.id)+"'><summary><a href='?q="+f.name+"'>"+f.name+"</a><a class='deleteBtn' href='/delete-folder/"+str(f.id)+"/'><i class='fa-solid fa-trash'></i></a></summary>"
                recurseDict(f, counter+1)
                foldersHTML+="</details>" 
        else:
            for f in folders.filter(previous_folder__name=parent_folder):
                foldersHTML+="<details id='folder-"+str(f.id)+"'><summary><a href='?q="+f.name+"'>"+"&nbsp &nbsp"*counter+f.name+"</a><a class='deleteBtn' href='/delete-folder/"+str(f.id)+"/'><i class='fa-solid fa-trash'></i></a></summary>"
                recurseDict(f, counter+1)
                foldersHTML+="</details>"
    if len(folders)>0:
        recurseDict(None, 0)
    decks_count = decks.count()
    context={'decks': decks, "folders":folders, "decks_count":decks_count, "foldersHTML":foldersHTML, "form":createDeckEmpty()}
    return render(request, "flashcards/home.html", context)

#@login_required
#def createFolder(request):
#    form = FolderForm(request.POST or None)
#    if form.is_valid():
#        formcreate=form.save(commit=False)
#        formcreate.user=request.user
#        formcreate.save()
#        return redirect('home')
#    form=FolderForm()
#    context={'form': form}
#    return render(request, 'flashcards/deck_form.html', context)

@login_required
def deckView(request, pk):
    print(request.user.id)
    print(Deck.objects.get(id=pk).folder)
    print(Deck.objects.get(id=pk).folder.id)
    context={
        "pk":pk,
        "user":request.user.id,
        "folder":Deck.objects.get(id=pk).folder.id,
        "folderList":Folder.objects.filter(user=request.user)
    }
    return render(request, "flashcards/deck.html", context)

# class FolderList(generics.ListCreateAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer


# class FolderDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Folder.objects.all()
#     serializer_class = FolderSerializer


# class DeckList(generics.ListCreateAPIView):
#     queryset=Deck.objects.all()
#     serializer_class = DeckSerializer

# class DeckDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Deck.objects.all()
#     serializer_class = DeckSerializer

@login_required
def DeckDetail(request, pk):
    deck=Deck.objects.get(id=pk)
    if deck.user==request.user:
        return JsonResponse(DeckSerializer(deck).data, status=200)
    return JsonResponse({}, status=404)

@login_required
def FlashcardList(request, pk):
    deck=Deck.objects.get(id=pk)
    flashcards=Flashcard.objects.filter(deck=deck)
    if deck.user==request.user:
        flashcardList=[]
        for x in flashcards:
            flashcardList.append(FlashcardSerializer(x).data)
        return JsonResponse({"flashcards":flashcardList}, status=200)
    return JsonResponse({}, status=404)


# class FlashcardList(generics.ListCreateAPIView):
#     def get_queryset(self):
#         deck=self.kwargs["deck"]
#   #      longitude = self.request.query_params.get('longitude')
#         queryset = Flashcard.objects.filter(deck=deck)
#         print(queryset)
#         return queryset
#     serializer_class = FlashcardSerializer


# class FlashcardDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Flashcard.objects.all()
#     def PUT(self, request, *args, **kwargs):
#         global queryset
#         flashcard = queryset
#         serializer = FlashcardSerializer(flashcard, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     serializer_class = FlashcardSerializer

@login_required
def updateJsonFlashcard(request, pk):
    form=FlashcardSerializer(data=request.POST or None)
    print(form)
    print(form.is_valid())
    print(form.data)
    print(form.errors)
    print("id is", form.validated_data.get("deck"))

    if form.is_valid():
        print("id is", form.validated_data.get("deck"))
        if form.validated_data.get("deck").user.id==request.user.id:
            flashcard=Flashcard.objects.get(id=pk)
            flashcard.key=form.validated_data["key"]
            print(flashcard.key)
            flashcard.answer=form.validated_data["answer"]
            print(form.validated_data["answer"])
            flashcard.deck=form.validated_data["deck"]
            flashcard.save()
         #   if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.data, status=201) #201=created items
           # form=DeckSerializer()
        #    return render("home.html")
        else:
            raise serializers.ValidationError("Page not found.")
    if form.errors:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
    context={'form': form}
    return render(request, 'flashcards/home.html', context)

@login_required
def updateJsonDeck(request, pk):
    form=DeckSerializer(data=request.POST or None)
    print(form)
    print(form.is_valid())
    print(form.errors)
    if form.is_valid():
        print (form.data.get("user"))
        print(request.user.id)
        if form.data.get("user")==request.user.id:
            name=form.validated_data.get("name")
            if name=="":
                raise serializers.ValidationError("deck name cannot be empty")
            deck=Deck.objects.get(id=pk)
            deck.name=form.data["name"]
            print(deck.name)
            deck.description=form.data["description"]
            deck.folder=Folder.objects.get(id=int(form.data["folder"]))
            deck.save()
         #   if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.data, status=201) #201=created items
           # form=DeckSerializer()
        #    return render("home.html")
        else:
            raise serializers.ValidationError("Page not found.")
    if form.errors:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
    context={'form': form}
    return render(request, 'flashcards/home.html', context)

@login_required
def deleteJsonFlashcard(request, pk):
    flashcard=Flashcard.objects.get(id=pk)
    print(flashcard.deck.user)
    if flashcard.deck.user.id==request.user.id:
        flashcard.delete()
        return JsonResponse({"message":"Deletion confirmed"}, status=201)
    raise JsonResponse({"message":"ERROR"}, status=400)


# @login_required
# def createFlashcard(request):
#     form = FlashcardSerializer(data=request.POST or None)
#     if form.is_valid():
#         if form.cleaned_data.get("deck").user==request.user:
#             form.save()
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse(form.data, status=201) #201=created items
#             form=FlashcardSerializer()
#             return redirect("deck", form.cleaned_data.get("deck"))
#         else:
#             raise form.ValidationError("No Access")
#     if form.errors:
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse(form.errors, status=400)
#     context={'form': form}
#     return render(request, 'flashcards/home.html', context)

# @login_required
# def createDeck(request):
#     form = DeckForm(request.POST or None)
#     print(form.is_valid)
#     print(form.data)
#     print(form.errors)
#     if form.is_valid():
#         deckcreate=form.save(commit=False)
#         deckcreate.user=request.user
#         deckcreate.save()
#         return redirect('home')
#     form=DeckForm()
#     folders = Folder.objects.filter(user=request.user)
#     context={'form': form, 'folders':folders}
#     return render(request, 'flashcards/deck_form.html', context)

# @login_required
# def updateDeck(request, pk):
#     deck = Deck.objects.get(id=pk)
#     if deck.user == request.user:
#         form = DeckForm(request.POST or None, instance=deck)
#         if form.is_valid():
#             deckupdate=form.save(commit=False)
#             deckupdate.user=request.user
#             deckupdate.save()
#             return redirect("home")
#         form=DeckForm()
#         context={'form':form}
#         return render(request, "flashcards/deck_form.html", context)
#     else:
#         raise Http404

@login_required
def deleteFolder(request, pk):
    folder= Folder.objects.get(id=pk)
    if folder.user == request.user:
        if request.method=="POST":
            folder.delete()
            return redirect("home")
        return render(request,"flashcards/delete.html", {'obj':folder})
    else:
        raise Http404

@login_required
def deleteDeck(request, pk):
    deck= Deck.objects.get(id=pk)
    if deck.user == request.user:
        if request.method=="POST":
            deck.delete()
            return redirect("home")
        return render(request,"flashcards/delete.html", {'obj':deck})
    else:
        raise Http404