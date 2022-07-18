import logging
logger = logging.getLogger(__name__)

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import AddChoiceForm
from .models import *
from .views_menu import menu, menu_log, get_menu


class VotedAnswerView(TemplateView):
    """answer/<int:survey_id>/    answer"""
    template_name = 'answer.html'
    extra_context = {'h3': 'fill the survey, please', 'title': 'vote'}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        context["menu"] = get_menu(self.request)

        context['survey_id'] = self.kwargs['survey_id']
        s = Survey.objects.get(id=self.kwargs['survey_id'])
        qs = Question.objects.filter(survey=s).order_by('id')
        context['questions'] = []
        for q in qs:
            cs = Choice.objects.filter(question=q)
            if cs:
                context['questions'].append((q, [c.choice for c in cs]))
        return context

    def save_choice(self, question, choice):
        a = Answer(answer=choice, question=question)
        a.save()

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        for q, opts in context['questions']:
            choice = request.POST.get(f"q{q.id}choice", None)
            if choice is None or choice in opts:
                # print(choice, choice in opts)
                question = Question.objects.get(id=q.id)
                self.save_choice(question, choice)
            else:
                raise Http404("choice incorrect")
        messages.success(self.request, 'voted')
        return HttpResponseRedirect(reverse('survey_app:home'))

  
class AddChoiceView(CreateView):
    """add-choice/<int:question_id>', name='add_choice'"""
    form_class = AddChoiceForm
    template_name = 'add_template.html'
    extra_context = {'h3': 'add answer choice', 'title': 'answer choice', "menu": menu_log + menu}
    
    def get_success_url(self):
        messages.success(self.request, 'added')
        return reverse_lazy('survey_app:question_detail', kwargs={'question_id': self.kwargs['question_id']}) 

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
