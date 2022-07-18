import logging
logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from .forms import *
from .models import *
from .views_menu import menu, menu_log

class AddQuestionView(CreateView):
    """add-question/<int:survey_id>/', name='add_question'"""
    form_class = AddQuestionForm
    template_name = 'add_template.html'
    extra_context = {'h3': 'add a question', 'title': 'add question', "menu": menu_log + menu}

    def get_success_url(self):
        messages.success(self.request, 'added')
        return reverse_lazy('survey_app:question_detail', kwargs={'question_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['survey_id']
        return context

    def get_queryset(self):
        num = self.kwargs['survey_id']
        surv_obj = Survey.objects.filter(id=num).first()
        return surv_obj

    def form_valid(self, form):
        form.instance.survey = self.get_queryset()
        # form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)



class DetailQuestionView(DetailView):
    "'question-detail/<int:pk>/', name='question_detail'"
    template_name = "queston_detail.html"
    model = Question
    extra_context = {'title': 'question', "menu": menu_log + menu}
    pk_url_kwarg = 'question_id'    # default: pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Choice.objects.filter(question=self.kwargs['question_id'])
        q = Question.objects.get(pk=self.kwargs['question_id'])
        # print(q)
        context['h3'] = q.question
        context['question_id'] = q.id
        context['data'] = data
        return context
