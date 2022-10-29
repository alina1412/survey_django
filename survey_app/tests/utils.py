from pathlib import WindowsPath

from django.urls import reverse

from survey_app.models import Choice, Question, Survey, User


def make_survey(user):
    Survey(title="Survey1", owner=user).save()
    surv = Survey.objects.filter().first()
    return surv


def make_question(survey):
    Question(question="first?", survey=survey).save()
    quest = Question.objects.filter().first()
    return quest


def add_survey_by_post(client):
    context = dict(title="Survey2")
    response = client.post(reverse("survey_app:add_survey"), context, follow=True)
    return response


def add_question_by_post(survey, client):
    context = dict(question="second?")
    response = client.post(
        reverse("survey_app:add_question", kwargs={"survey_id": survey.id}),
        context,
        follow=True,
    )
    return response


def add_choice_by_post(question, client):
    context = dict(choice="-choice1")
    response = client.post(
        reverse("survey_app:add_choice", kwargs={"question_id": question.id}),
        context,
        follow=True,
    )
    return response


def resp200_survey_detail(survey, client):
    response = client.get(
        reverse("survey_app:survey_detail", kwargs={"survey_id": survey.id}),
        follow=True,
    )
    return response


def resp200_question_detail(question, client):
    response = client.get(
        reverse("survey_app:question_detail", kwargs={"question_id": question.id}),
        follow=True,
    )
    return response


def delete_question_by_checkbox(survey, question, client):
    assert Question.objects.all().count() == 2
    data = {"delete": True, str(question.id): "on"}
    response = client.post(
        reverse("survey_app:survey_detail", kwargs={"survey_id": survey.id}),
        data=data,
        follow=True,
    )
    return response


def test_registered_templates(client, url_to_reverse):
    survey_id = Survey.objects.first().id
    response = client.get(
        reverse(url_to_reverse, kwargs={"survey_id": survey_id}),
    )
    temps = [
        x.__str__() if isinstance(x, WindowsPath) else x
        for x in [t.name for t in response.templates]
    ]
    return response, temps


def create_second_user(client):
    user2 = User.objects.create(username="user2", password="qwerty12542")
    client.force_login(user2)
    return user2


def get_response_from_url_with_follow(client, url_to_reverse, kwargs, context={}):
    response = client.get(
        reverse(url_to_reverse, kwargs=kwargs), context=context, follow=True
    )
    return response
