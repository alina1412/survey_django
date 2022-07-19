import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import AddChoiceForm
from .models import *
from .views_menu import menu, menu_log, get_menu
from .view_mixin import LoginRequiredMixin

class VotedAnswerView(TemplateView):
    """answer/<int:survey_id>/    answer"""
    template_name = 'answer.html'
    extra_context = {'h3': 'fill the survey, please', 'title': 'vote'}
    
    def get_survey(self, survey_id):
        try:
            survey_obj = Survey.objects.get(id=survey_id)
            return survey_obj
        except ObjectDoesNotExist:
            raise Http404

    def get_questions_of_a_survey(self, survey):
        return Question.objects.filter(survey=survey).order_by('id')

    def get_question_list_and_choices(self, questions):
        q_tuples = []
        for q in questions:
            cs = Choice.objects.filter(question=q)
            print(cs)
            if cs:
                q_tuples.append((q, [c.choice for c in cs]))
        # print(q_tuples)
        return q_tuples

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        context["menu"] = get_menu(self.request)
        survey_id = self.kwargs['survey_id']
        context['survey_id'] = survey_id
        survey_obj = self.get_survey(survey_id)
        # print(survey_obj)
        qs = self.get_questions_of_a_survey(survey_obj)
        # print(qs)
        context['questions'] = self.get_question_list_and_choices(qs)
        # print(context['questions'])
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

  
class AddChoiceView(LoginRequiredMixin, CreateView):
    """add-choice/<int:question_id>', name='add_choice'"""
    form_class = AddChoiceForm
    template_name = 'add_template.html'
    extra_context = {'h3': 'add answer choice', 
                     'title': 'answer choice',
                     "menu": menu + menu_log}
    
    def get_success_url(self):
        # messages.success(self.request, 'added')
        return reverse_lazy('survey_app:question_detail', kwargs={'question_id': self.kwargs['question_id']}) 

    def check_ownership(self, survey_id):
        try:
            surv = Survey.objects.get(id=survey_id)
        except ObjectDoesNotExist:
            raise Http404
        if surv.owner.id != self.request.user.id:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['pk'] = self.kwargs['question_id']
        q_obj = self.get_queryset()
        self.check_ownership(q_obj.survey.id)
        return context

    def get_queryset(self):
        num = self.kwargs['question_id']
        try:
            q_obj = Question.objects.get(id=num)
        except ObjectDoesNotExist:
            raise Http404
        return q_obj

    def form_valid(self, form):
        form.instance.question = self.get_queryset()
        # form.instance.
        # form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)
