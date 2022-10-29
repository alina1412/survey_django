import logging

from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from survey_app.crud import (
    get_choices_of_question,
    get_question_by_question_id,
    get_questions_of_a_survey,
    get_survey_by_id,
)
from survey_app.forms import AddChoiceForm
from survey_app.models import Answer
from survey_app.views.view_mixin import LoginRequiredMixin
from survey_app.views.utils import get_menu, menu, menu_log

logger = logging.getLogger(__name__)


class VotedAnswerView(TemplateView):
    """answer/<int:survey_id>/    answer"""

    template_name = "answer.html"
    extra_context = {"h3": "fill the survey, please", "title": "vote"}

    def get_question_list_and_choices(self, questions):
        q_tuples = []
        for q in questions:
            cs = get_choices_of_question(q)
            print(cs)
            if cs:
                q_tuples.append((q, [c.choice for c in cs]))
        return q_tuples

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        context["menu"] = get_menu(self.request)
        survey_id = self.kwargs["survey_id"]
        context["survey_id"] = survey_id
        survey_obj = get_survey_by_id(survey_id)
        qs = get_questions_of_a_survey(survey_obj).order_by("id")
        context["questions"] = self.get_question_list_and_choices(qs)
        return context

    def save_choice(self, choice, question):
        a = Answer(answer=choice, question=question)
        a.save()

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        for q, opts in context["questions"]:
            choice = request.POST.get(f"q{q.id}choice", None)
            if choice is None or choice in opts:
                question = get_question_by_question_id(q.id)
                self.save_choice(choice, question)
            else:
                raise Http404("choice incorrect")
        messages.success(self.request, "voted")
        return HttpResponseRedirect(reverse("survey_app:home"))


class AddChoiceView(LoginRequiredMixin, CreateView):
    """add-choice/<int:question_id>', name='add_choice'"""

    form_class = AddChoiceForm
    template_name = "add_template.html"
    extra_context = {
        "h3": "add answer choice",
        "title": "answer choice",
        "menu": menu + menu_log,
    }

    def get_success_url(self):
        # messages.success(self.request, 'added')
        return reverse_lazy(
            "survey_app:question_detail",
            kwargs={"question_id": self.kwargs["question_id"]},
        )

    def check_ownership(self, survey):
        if survey.owner.id != self.request.user.id:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q_obj = self.get_queryset()
        survey = get_survey_by_id(q_obj.survey.id)
        self.check_ownership(survey)
        return context

    def get_queryset(self):
        return get_question_by_question_id(self.kwargs["question_id"])

    def form_valid(self, form):
        form.instance.question = self.get_queryset()
        form.save()
        return super().form_valid(form)
