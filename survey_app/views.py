import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView 
from django.views.generic import CreateView

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .forms import *
from .models import *
from .views_menu import menu, menu_param, menu_log
from .views_choices_answers import *
from .views_survey import *
from .views_questions import *


def home_view(request):
    return render(request, 'home.html', 
            {'h3': 'To make and answer surveys is easy',
                    'image': "img_path", "menu": menu})
    # return HttpResponse("Hello World")

def logout_view(request):
    logout(request)
    messages.success(request, 'logged out')
    return HttpResponseRedirect(reverse('survey:home'))

class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm
    model = User
    extra_context = {'title': 'register', 'h3': 'Register for creating surveys', "menu": menu}

    def get_success_url(self): 
        messages.success(self.request, 'registered')
        return reverse_lazy('survey:login')

    def form_valid(self, form):
        form.save()
        # username = form.cleaned_data.get('username')
        # raw_password = form.cleaned_data.get('password1')
        # print(username, raw_password)
        return super().form_valid(form)

        
class SurveyLoginView(LoginView):
    template_name = "login.html"
    form_class = AuthenticationForm
    extra_context = {'title': 'login', 'h3': 'Login', "menu": menu}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('survey:survey_list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user) 
        messages.success(self.request, 'logged in')
        return HttpResponseRedirect(self.get_success_url())
        
    def form_invalid(self, form):
        messages.error(self.request, 'wrong username or password')
        return self.render_to_response(self.get_context_data(form=form))
