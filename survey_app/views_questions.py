import logging

from django.http import Http404
logger = logging.getLogger(__name__)

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

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
        messages.success(self.request, 'added')
        return reverse_lazy('survey_app:question_detail', kwargs={'question_id': self.object.pk})

    def check_ownership(self, survey_id):
        try:
            surv = Survey.objects.get(id=survey_id)
        except ObjectDoesNotExist:
            raise Http404
        if surv.owner.id != self.request.user.id:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.check_ownership(self.kwargs['survey_id'])
        # context['pk'] = self.kwargs['survey_id']
        return context

    def get_queryset(self):
        num = self.kwargs['survey_id']
        surv_obj = Survey.objects.filter(id=num).first()
        return surv_obj

    def form_valid(self, form):
        # if not self.form_invalid(form):
        form.instance.survey = self.get_queryset()
        # form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)
    
    # def form_invalid(self, form):
    #     surv_obj = self.get_queryset()
    #     if not surv_obj or (surv_obj.owner.id != self.request.user.id):
    #         raise Http404
    #     return super().form_invalid(form)


class DetailQuestionView(LoginRequiredMixin, DetailView):
    "'question-detail/<int:question_id>/', name='question_detail'"
    template_name = "queston_detail.html"
    model = Question
    extra_context = {'title': 'question', "menu": menu + menu_log}
    pk_url_kwarg = 'question_id'    # default: pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = Question.objects.get(pk=self.kwargs['question_id'])
        if not q or (q.survey.owner.id != self.request.user.id):
            raise Http404
        data = Choice.objects.filter(question=self.kwargs['question_id'])
        
        # print(q)
        context['h3'] = q.question
        context['question_id'] = q.id
        context['data'] = data
        return context
