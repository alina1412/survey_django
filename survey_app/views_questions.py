import logging
logger = logging.getLogger(__name__)

from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from .crud import *
from .forms import *
from .models import *
from .views_menu import menu, menu_log
from .view_mixin import LoginRequiredMixin


class AddQuestionView(LoginRequiredMixin, CreateView):
    """add-question/<int:survey_id>/', name='add_question'"""
    form_class = AddQuestionForm
    template_name = 'add_template.html'
    extra_context = {'h3': 'add a question', 'title': 'add question', "menu": menu + menu_log}

    def get_success_url(self):
        # messages.success(self.request, 'added')
        return reverse_lazy('survey_app:question_detail', kwargs={'question_id': self.object.pk})

    def check_ownership(self, survey):
        if survey.owner.id != self.request.user.id:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        surv_obj = get_survey_by_id(self.kwargs['survey_id'])
        self.check_ownership(surv_obj)
        context['survey'] = surv_obj
        return context

    def form_valid(self, form):
        form.instance.survey = self.get_context_data()['survey']
        form.save()
        return super().form_valid(form)
    

class DetailQuestionView(LoginRequiredMixin, DetailView):
    "'question-detail/<int:question_id>/', name='question_detail'"
    template_name = "queston_detail.html"
    model = Question
    extra_context = {'title': 'question', "menu": menu + menu_log}
    pk_url_kwarg = 'question_id'    # default: pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = get_question_by_question_id(self.kwargs['question_id'])
        if not q or (q.survey.owner.id != self.request.user.id):
            raise Http404
        data = get_choices_of_question(q)  
        # print(q)
        context['h3'] = "Question: " + q.question
        context['question_id'] = q.id
        context['data'] = data
        return context
