
from django import forms
from .models import  Question, Survey, Choice
from django.contrib.auth.forms import UserCreationForm


class CreateSurvey(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title']


class AddQuestionForm(forms.ModelForm):
    question = forms.CharField(label="question", max_length=200)

    class Meta:
        model = Question
        fields = ['question']


class AddChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice']








