from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import *


def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise Http404


def get_survey_by_id(survey_id):
    try:
        survey_obj = Survey.objects.get(id=survey_id)
        return survey_obj
    except ObjectDoesNotExist:
        raise Http404


def get_question_by_question_id(question_id):
    try:
        q_obj = Question.objects.get(id=question_id)
    except ObjectDoesNotExist:
        raise Http404
    return q_obj


def get_questions_of_a_survey(survey_obj):
    return Question.objects.filter(survey=survey_obj)


def get_qset_questions_of_survey(survey_id):
    return Question.objects.\
                    select_related('survey').\
                    filter(survey__id=survey_id) 


def get_owned_surveys(user_id):
    return Survey.objects.select_related('owner').\
                          filter(owner__id = user_id)  


def get_choices_of_question(question):
    return Choice.objects.filter(question=question)


def get_qset_answers_for_question(question):
    return Answer.objects.filter(question=question)


def get_user_by_name(username):
    return User.objects.filter(username=username).first()


def get_or_create_demo_user():
    demo_username = 'demo_djando_user_for_suveys'
    demo_password = 'demo_user_password'
    user = get_user_by_name(demo_username)
    if not user:
        user = User.objects.create_user(username=demo_username, password=demo_password)
        user.save()
    return user