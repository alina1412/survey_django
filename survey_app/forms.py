from dataclasses import fields
import enum

from django import forms
from .models import Question, Survey


class CreateSurvey(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title']


class AddQuestionForm(forms.ModelForm):
    question = forms.CharField(label="question", max_length=200)

    class Meta:
        model = Question
        fields = ['question']


ShopUnitType = enum.Enum("ShopUnitType", [
    ("OFFER", "OFFER"),
    ("CATEGORY", "CATEGORY")
])

class OptionForm(forms.Form):
    choice = forms.ChoiceField(choices = ShopUnitType) 
