

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


class VotedAnswerView(TemplateView):
    """answer/<int:survey_id>/    answer"""
    template_name = 'answer.html'
    extra_context = {'h3': 'fill the survey, please', 'title': 'fill answer'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey_id'] = self.kwargs['survey_id']
        s = Survey.objects.get(id=self.kwargs['survey_id'])
        qs = Question.objects.filter(survey=s).order_by('id')
        context['questions'] = []
        for q in qs:
            cs = Choice.objects.filter(question=q)
            if cs:
                context['questions'].append((q, [c.choice for c in cs])) #c.choice for c in cs
        return context

    def save_choice(self, question, choice):
        a = Answer(answer=choice, question=question)
        a.save()

    def post(self, request, *args, **kwargs):
        # NUM = 1
        context = self.get_context_data()
        # len_questions = len(context['questions'])
        # print(context['questions'])
        for q, opts in context['questions']:
            choice = request.POST.get(f"q{q.id}choice", None)
            if choice is None or choice in opts:
                print(choice, choice in opts)
                question = Question.objects.get(id=q.id)
                self.save_choice(question, choice)
            else:
                raise Http404("choice incorrect")

        return HttpResponse(f"--{choice}")

  
  

class AddChoiceView(CreateView):
    """add-choice/<int:question_id>', name='add_choice'"""
    # model = Question
    # fields = ['question']
    form_class = AddChoiceForm
    template_name = 'add_template.html'
    extra_context = {'h3': 'add answer choice', 'title': 'answer choice'}
    
    def get_success_url(self):
        return reverse_lazy('survey:question_detail', kwargs={'pk': self.kwargs['question_id']}) #TODO  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['question_id']
        return context

    def get_queryset(self):
        num = self.kwargs['question_id']
        q_obj = Question.objects.get(id=num)
        return q_obj

    def form_valid(self, form):
        form.instance.question = self.get_queryset()
        # form.instance.
        # form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)




# class AnswerPageView(CreateView):
#     template_name = "answer.html"
#     form_class = VoteForm
#     extra_context = {'title': 'answer'}

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(kwargs if kwargs else '-')
#         return context


class RegisterView(ListView):
    template_name = "home.html"

class LoginView(ListView):
    template_name = "home.html"





        
        
        # 