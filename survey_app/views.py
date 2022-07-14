

import logging
from typing import Optional, Type
logger = logging.getLogger(__name__)

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import *
from .forms import *
from .questions_views import *
from .survey_views import *
from django.views.generic import TemplateView, DetailView, ListView, CreateView
 

def home_view(request):
    return HttpResponse("Hello World")


# def create_view(request):
#     form = CreateNewList()
#     return render(request, 'create.html', {'form': form})







class AnswerPageView(CreateView):
    template_name = "answer.html"
    form_class = OptionForm
    extra_context = {'title': 'answer'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs if kwargs else '-')
        return context


class RegisterView(ListView):
    template_name = "home.html"

class LoginView(ListView):
    template_name = "home.html"





        
        
        # 