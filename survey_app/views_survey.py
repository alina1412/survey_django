import logging

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from survey_app.crud import (
    get_choices_of_question,
    get_owned_surveys,
    get_qset_answers_for_question,
    get_qset_questions_of_survey,
    get_questions_of_a_survey,
    get_survey_by_id,
    get_user_by_id,
)
from survey_app.download import AttachFile
from survey_app.forms import CreateSurvey
from survey_app.models import Survey
from survey_app.view_mixin import LoginRequiredMixin
from survey_app.views_menu import get_menu, menu, menu_log, menu_notlog

logger = logging.getLogger(__name__)


class AddSurveyView(LoginRequiredMixin, CreateView):
    """'add-survey/' name='add_survey'"""

    template_name = "add_template.html"
    form_class = CreateSurvey
    # print( menu + menu_log)
    extra_context = {
        "title": "add survey",
        "h3": "add a survey",
        "menu": menu + menu_log,
    }
    # context_object_name = 'object_list'

    def get_success_url(self):
        messages.success(self.request, "added")
        return reverse("survey_app:survey_list")

    def form_valid(self, form):
        form.instance.owner = get_user_by_id(self.request.user.id)
        form.save()
        return super().form_valid(form)


class DetailSurveyView(LoginRequiredMixin, DetailView):
    """'survey-detail/<int:survey_id>/', name='survey_detail'"""

    model = Survey
    template_name = "survey_detail.html"
    extra_context = {"title": "survey detail", "menu": menu + menu_log}
    pk_url_kwarg = "survey_id"  # default: pk

    def check_ownership(self, survey):
        if survey.owner.id != self.request.user.id:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = get_survey_by_id(self.kwargs["survey_id"])
        self.check_ownership(survey)
        questions = get_questions_of_a_survey(survey)
        context["data"] = questions
        context["survey"] = survey
        context["h3"] = survey.title
        return context

    def post(self, request, *args, **kwargs):
        if "delete" in request.POST:
            # print("delete")
            survey = get_survey_by_id(self.kwargs["survey_id"])
            for item in get_questions_of_a_survey(survey):
                x = request.POST.get(str(item.id), "off")
                if x == "on":
                    item.delete()

        if "download" in request.POST:
            survey = get_survey_by_id(self.kwargs["survey_id"])
            questions = get_questions_of_a_survey(survey)
            return self.get_file_to_attach(questions)

        return redirect("survey_app:survey_detail", survey_id=self.kwargs["survey_id"])

    def get_file_to_attach(self, item_list):
        AF = AttachFile(item_list)
        return AF.attach_file()


class OwnedListSurveysView(LoginRequiredMixin, ListView):
    """'surveys/', name='survey_list'"""

    template_name = "surveys_list.html"
    model = Survey
    context_object_name = "object_list"
    extra_context = {"menu": menu + menu_log}

    def get_queryset(self):
        return get_owned_surveys(self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        # print(context['object_list'])
        context["title"] = "survey list"
        context["h3"] = "your survey's list"
        return context

    def post(self, request):
        if "delete" in request.POST:
            # print("delete")
            for item in self.get_queryset():
                x = request.POST.get(str(item.id), "off")
                if x == "on":
                    item.delete()
        return redirect("survey_app:survey_list")


class SurveyToPassView(ListView):
    """'surveys/', name='survey_list'"""

    template_name = "surveys_to_pass_list.html"
    model = Survey
    context_object_name = "object_list"
    extra_context = {"h3": "surveys you can pass", "title": "to pass"}

    # def get_queryset(self):
    #     return Survey.objects.filter()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        context["menu"] = menu_notlog + menu
        context["menu"] = get_menu(self.request)
        return context


class ResultsView(LoginRequiredMixin, ListView):
    template_name = "results.html"
    extra_context = {"h3": "results of a survey", "title": "results"}

    def check_ownership(self, survey):
        if survey.owner.id != self.request.user.id:
            raise Http404

    def get_count_votes_for_choice(self, qset_answers, ch):
        return qset_answers.filter(answer=ch.choice).count()

    def get_item_answer_statistic(self, question):
        item = {}
        qset_answers = get_qset_answers_for_question(question)
        choices = get_choices_of_question(question)

        choice_name_count = []
        for choice in choices:
            ans_count = self.get_count_votes_for_choice(qset_answers, choice)
            choice_name_count.append((choice, ans_count))
        item["choices"] = choice_name_count if choice_name_count else ("", "")
        item["title"] = question.question
        return item

    def get_queryset(self):
        """object_list of items:
        item['title'] = question.question;
        item['choices'] = [(choice, its_ans_count)]"""
        object_list = []
        survey_id = self.kwargs["survey_id"]
        survey = get_survey_by_id(survey_id)
        self.check_ownership(survey)
        q_set = get_qset_questions_of_survey(survey_id)
        for question in q_set:
            item = self.get_item_answer_statistic(question)
            object_list.append(item)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        context["menu"] = get_menu(self.request)
        return context
