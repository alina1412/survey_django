import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
 
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView, CreateView

from .views_menu import menu, menu_log, menu_notlog, get_menu

class AddSurveyView(CreateView): # LoginRequiredMixin
    """'add-survey/' name='add_survey'"""
    template_name = "add_template.html"
    form_class = CreateSurvey
    # print( menu_log + menu)
    extra_context = {'title': 'add survey', 'h3': 'add a survey', "menu": menu_log + menu}
    # context_object_name = 'object_list'

    def get_success_url(self): 
        messages.success(self.request, 'added')
        return reverse('survey_app:survey_list')

    def form_valid(self, form):
        form.instance.owner = User.objects.get(id=self.request.user.id)
        form.save()
        return super().form_valid(form)


from .download import AttachFile
class DetailSurveyView(DetailView):
    """'survey-detail/<int:survey_id>/', name='survey_detail'"""
    model = Survey
    template_name = 'survey_detail.html'
    extra_context = {'title': 'survey detail', "menu": menu_log + menu}
    pk_url_kwarg = 'survey_id'  # default: pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        surv = Survey.objects.get(id=self.kwargs['survey_id'])
        if not surv:
            return Http404
        questions = Question.objects.filter(survey=self.kwargs['survey_id'])
        context['data'] = questions
        context['survey'] = surv
        context['h3'] = surv.title
        return context

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            # print("delete")
            for item in Question.objects.filter(survey=self.kwargs['survey_id']):
                x = request.POST.get(str(item.id), 'off')
                if x == 'on':
                    item.delete()

        if 'download' in request.POST:
            questions = Question.objects.filter(survey=self.kwargs['survey_id'])
            return self.get_file_to_attach(questions)

        return redirect('survey_app:survey_detail', survey_id=self.kwargs['survey_id'])
    
    def get_file_to_attach(self, item_list):
        AF = AttachFile(item_list)
        return AF.attach_file()

class OwnedListSurveysView(ListView):
    """'surveys/', name='survey_list'"""
    template_name = "surveys_list.html"
    model = Survey
    context_object_name = 'object_list'
    extra_context = {"menu": menu_log + menu}

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
        context['h3'] = "your survey's list"
        return context

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            # print("delete")
            for item in self.get_queryset():
                x = request.POST.get(str(item.id), 'off')
                if x == 'on':
                    item.delete()
        return redirect('survey_app:survey_list')


class SurveyToPassView(ListView):
    """'surveys/', name='survey_list'"""
    template_name = "surveys_to_pass_list.html"
    model = Survey
    context_object_name = 'object_list'
    extra_context = {'h3': 'survey you can pass', 'title': 'to pass'}

    def get_queryset(self):
        return Survey.objects.filter()  
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        context["menu"] = menu_notlog + menu
        context["menu"] = get_menu(self.request)
        return context


class ResultsView(ListView):
    template_name = "results.html"
    extra_context = {'h3': 'results of a survey', 'title': 'results'}

    def get_qset_questions_of_survey(self, survey_id):
        return Question.objects.\
                        select_related('survey').\
                        filter(survey__id=survey_id) 

    def get_qset_answers_for_question(self, question):
        return Answer.objects.filter(question=question)

    def get_qset_choices_for_question(self, question):
        return Choice.objects.filter(question=question)

    def get_count_votes_for_choice(self, qset_answers, ch):
        return qset_answers.filter(answer=ch.choice).count()

    def get_item_answer_statistic(self, question):
        item = {}
        qset_answers = self.get_qset_answers_for_question(question)
        choices = self.get_qset_choices_for_question(question)

        choice_name_count = []
        for choice in choices:
            ans_count = self.get_count_votes_for_choice(qset_answers, choice)
            choice_name_count.append((choice, ans_count))
        item['choices'] = choice_name_count if choice_name_count else ("", "")
        item['title'] = question.question
        return item

    def get_queryset(self):
        """object_list of items:
        item['title'] = question.question; 
        item['choices'] = [(choice, its_ans_count)] """
        object_list = [] 
        q_set = self.get_qset_questions_of_survey(self.kwargs['survey_id'])
        for question in q_set:
            item = self.get_item_answer_statistic(question)
            object_list.append(item)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        context["menu"] = get_menu(self.request)
        return context
