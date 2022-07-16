

import logging
from typing import Optional, Type
logger = logging.getLogger(__name__)

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
 
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView, CreateView


class AddSurveyView(CreateView): # LoginRequiredMixin
    """'add-survey/' name='add_survey'"""
    template_name = "add_template.html"
    form_class = CreateSurvey
    extra_context = {'title': 'add survey', 'h3': 'add a survey'}
    # context_object_name = 'object_list'

    def get_success_url(self): 
        return reverse('survey:survey_list')

    def form_valid(self, form):
        form.instance.owner = User.objects.get(id=self.request.user.id)
        form.save()
        return super().form_valid(form)


class DetailSurveyView(DetailView):
    """'survey-detail/<int:pk>/', name='survey_detail'"""
    model = Survey
    template_name = 'survey_detail.html'
    extra_context = {'title': 'survey detail'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        surv = Survey.objects.get(id=self.kwargs['pk'])
        if not surv:
            return Http404
        questions = Question.objects.filter(survey=self.kwargs['pk'])
        context['data'] = questions
        context['survey'] = surv
        context['h3'] = surv.title
        return context

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            # print("delete")
            for item in Question.objects.filter(survey=self.kwargs['pk']):
                x = request.POST.get(str(item.id), 'off')
                if x == 'on':
                    item.delete()
        return redirect('survey:survey_detail', pk=self.kwargs['pk'])


class ListSurveysView(ListView):
    """'surveys/', name='survey_list'"""
    template_name = "surveys_list.html"
    model = Survey
    context_object_name = 'object_list'

    def get_queryset(self):
        return Survey.objects.\
                        select_related('owner').\
                        filter(owner__id = self.request.user.id)  
                      #  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        print(context['object_list']) 
        context['title'] = 'survey list'
        context['h3'] = 'survey list'
        return context

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            # print("delete")
            for item in self.get_queryset():
                x = request.POST.get(str(item.id), 'off')
                if x == 'on':
                    item.delete()
        return redirect('survey:survey_list')
