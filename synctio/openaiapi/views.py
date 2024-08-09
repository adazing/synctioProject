from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse, HttpResponse
from flashcards.forms import DeckForm, FolderForm, FlashcardForm, findFlashcardForm

from flashcards.models import Flashcard, FlashcardImpression
from flashcards.serializers import FlashcardSerializer
# Create your views here.
import os
import openai
#from flask import Flask, redirect, render_template, request, url_for
from .forms import answerForm, flashcardIdForm
openai.api_key = os.getenv("OPENAI_API_KEY")
import re
from collections import OrderedDict
import random
from .serializers import FlashcardInformation
import random
import vowpalwabbit

closestNum=0.8


def flashcardfindapiview(request):
    form=findFlashcardForm(request.POST or None)
    print(form.is_valid)
    if form.is_valid():
        currentFlashcard=Flashcard.objects.get(id=form.cleaned_data.get('flashcard'))
        review=form.cleaned_data.get('review')
        if review=="1" or review=="0":
            currentFlashcardImpression=FlashcardImpression.objects.create(user=request.user, flashcard=currentFlashcard, review=review)
            currentFlashcardImpression.save()
        '''
            create dictionary for deck with
            key: abs(flashcard levelknown/5-closestNum)
            value: flashcard id
            then sort and find best flashcard to give next
        '''
        model = vowpalwabbit.Workspace(quiet=True)
        try:
            flashcardImpressions=FlashcardImpression.objects.filter(user=request.user, flashcard=currentFlashcard)
            flashcards=Flashcard.objects.filter(deck=currentFlashcard.deck)
            for x in flashcardImpressions:
                foo=str(x.review)+" | user_id:"+str(x.user.id)+" flashcard_id:"+str(x.flashcard.id)+" key_length:"+str(len(x.flashcard.key))+" answer_length:"+str(len(x.flashcard.answer))
                print(foo)
                model.learn(foo)
            bestVal=1.0
            nextFlashcard=None
            for p in flashcards:
                flashPred=model.predict("| user_id:"+str(request.user.id)+" flashcard_id:"+str(p.id)+" key_length:"+str(len(p.key))+" answer_length:"+str(len(p.answer)))
                print('prediction')
                print(flashPred)
                print(p)
                print(currentFlashcard)
                if flashPred<=0.8 and p!=currentFlashcard:
                    if 0.8-flashPred<bestVal:
                        bestVal=0.8-flashPred
                        nextFlashcard=p
            if nextFlashcard==None:
                listFlash=list(Flashcard.objects.filter(deck=currentFlashcard.deck))
                listFlash.remove(currentFlashcard)
                for flash in Flashcard.objects.filter(deck=currentFlashcard.deck):
                    FlashcardImpression.objects.filter(user=request.user, flashcard=flash).delete()
                    nextFlashcard = random.choice(listFlash)
            print("endtry")
        except:
            listFlash=list(Flashcard.objects.filter(deck=currentFlashcard.deck))
            listFlash.remove(currentFlashcard)
            for flash in Flashcard.objects.filter(deck=currentFlashcard.deck):
                FlashcardImpression.objects.filter(user=request.user, flashcard=flash).delete()
                print(list(Flashcard.objects.filter(deck=currentFlashcard.deck)).remove(currentFlashcard))
            nextFlashcard = random.choice(listFlash)
            print("endexcept")
        print("answer is "+nextFlashcard.answer)
        serializer={"key":nextFlashcard.key, "answer":nextFlashcard.answer, "id":nextFlashcard.id}
        if len(nextFlashcard.answer)>=50:
            response=openai.Completion.create(
                model="text-davinci-002",
                prompt=generate_prompt2(nextFlashcard.answer.lower()),
                temperature=1.0,
                max_tokens=6,
            )
            textresponse=response.choices[0].text
            print(textresponse)
#            if findWholeWord(textresponse)(currentFlashcard.answer):
            if textresponse in nextFlashcard.answer:
                serializer={"key":nextFlashcard.key+" <br><br> "+nextFlashcard.answer.replace(textresponse, "_____"), "answer":textresponse, "id":nextFlashcard.id}
                return JsonResponse(serializer, status=200)
            else:
                print("hello")
                randWord=random.choice(nextFlashcard.answer.split())
                print(randWord)
                serializer={"key":nextFlashcard.key+" <br><br> "+nextFlashcard.answer.replace(randWord, "_____"), "answer":randWord, "id":nextFlashcard.id}
                return JsonResponse(serializer, status=200)
        return JsonResponse(serializer, status=200)
    return JsonResponse({}, status=404)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


# def processor(request):
#     form=flashcardIdForm(request.POST or None)
#     print(form.is_valid)
#     print(form)
#     print(form.errors)
#     if form.is_valid():
#         flashcard=Flashcard.objects.get(id=form.cleaned_data['flashcard'])
#         print(flashcard.answer)
#         if len(flashcard.answer)>=50:
#             flashcard=Flashcard.objects.get(id=form.cleaned_data['flashcard'])
#             print(flashcard.answer)
#             print('hi')
#             response=openai.Completion.create(
#                 model="text-ada-001",
#                 prompt=generate_prompt2(flashcard.answer),
#                 temperature=0.5,
#                 max_tokens=6,
#             )
#             textresponse=response.choices[0].text
#             print(textresponse)
#             if findWholeWord(textresponse)(flashcard.answer):
#                 return JsonResponse({"response":textresponse, "index":flashcard.answer.find(textresponse)}, status=200)
#             else:
#                 return JsonResponse({"response":flashcard.answer.split()[0], "index":0}, status=200)
# #return findword(request)
#     return JsonResponse({"response":"none"})


# def findword(request):
#     form=flashcardIdForm(request.POST or None)
#     if form.is_valid():
#         flashcard=Flashcard.objects.get(id=form.cleaned_data['flashcard'])
#         response=openai.Completion.create(
#             model="text-davinci-002",
#             prompt=generate_prompt2(flashcard.answer),
#             temperature=0.0,
#             max_tokens=6,
#         )
#         textresponse=response.choices[0].text
#         if textresponse in flashcard.answer:
#             return JsonResponse({"response":textresponse}, status=200)
#         else:
#             return JsonResponse({"response":flashcard.answer.split()[0]}, status=200)
        
    
def check(request):
    form=answerForm(request.POST or None)
    print(form.is_valid)
    print("checking")
    if form.is_valid():
        answer = form.cleaned_data["answer"]
        flashcard=Flashcard.objects.get(id=form.cleaned_data['flashcard'])
        flashcardAnswer=form.cleaned_data["flashcardAnswer"]
        print("hi")
        if len(flashcard.answer)<50:
            flashcardAnswer=flashcard.answer
            
        if answer==flashcardAnswer:
            return JsonResponse({"response":"1"}, status=200)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(flashcardAnswer.lower(), answer.lower()),
            temperature=0.0,
            max_tokens=6,
        )
            
        textresponse=response.choices[0].text
        print(textresponse)
        if textresponse.upper()!="YES" and textresponse.upper()!="NO":
            return JsonResponse({"response":"0"}, status=200)
        if textresponse.upper()=="YES":
            return JsonResponse({"response":"1"}, status=200)
        else:
            return JsonResponse({"response":"0"}, status=200)
    return JsonResponse({"response":"0"}, status=200)

def generate_prompt(original, answer):
    return f"""Return Boolean (YES or NO) if the two pieces of text are similar and are in the same language:
Sentence 1:a line, segment, or ray that cuts a segment into two equal parts
Sentence 2:a segment.
Answer:NO

Sentence 1:gracias.
Sentence 2:muchas gracias!
Answer:YES

Sentence 1:la galleta
Sentence 2:galleta
Answer:YES

Sentence 1:thanks
Sentence 2:gracias!
Answer:NO

Sentence 1:{original.lower()}
Sentence 2:{answer.lower()}
Answer:"""

def generate_prompt2(original):
    return f"""Return the most important word of the sentence.
Sentence:a line, segment, or ray that cuts a segment into two equal parts.
Answer:ray

Sentence:one of the most famous complementary colors are that of blue and orange.
Answer:complementary


Sentence:{original.lower()}
Answer:"""