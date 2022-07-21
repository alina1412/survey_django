from pathlib import WindowsPath
# from django.test import SimpleTestCase, TestCase, Client
# from django import urls
import pytest

from .models import *
from .views import *

import logging
logger = logging.getLogger(__name__)


# pytest-django has a build-in fixture client
@pytest.fixture()
def auto_login_user(db, client):
    print()
    print("fixture\n")
    user = User.objects.create(username="user1", password="qwerty12542")
    client.force_login(user)
    return client, user


@pytest.mark.django_db
def test_user(auto_login_user):
    client, user = auto_login_user
    count = User.objects.all().count()
    assert count == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    'param', [
        'survey_app:home',
        'survey_app:surveys_to_pass',
        'survey_app:register',
        'survey_app:login'
    ]
)
def test_get200_request(param, client):
    response = client.get(reverse(param), follow=True)
    assert response.status_code == 200

# @pytest.mark.parametrize(
#         'param', [
#             '/shelves/books_add/',
#             '/shelves/table_books/'
#         ]
#     )
# def test_unauthorized_request(param, client):
#    response = client.get(param, follow=True)
#    assert b"login" in response.content


@pytest.mark.django_db
@pytest.mark.parametrize(
    'param', [
        'survey_app:add_survey',
        'survey_app:register',
        'survey_app:login',
        'survey_app:survey_list',
    ]
)
def test_url_list(param, auto_login_user):
    client, user = auto_login_user
    response = client.get(reverse(param))
    assert response.status_code == 200
#     assert b'table of books' in response.content
#     assert b'example_author_' in response.content


@pytest.mark.django_db
def test_pages_with_db(auto_login_user):
    client, user = auto_login_user

    def make_survey():
        Survey(title='Survey1', owner=user).save()
        surv = Survey.objects.filter().first()
        count = Survey.objects.all().count()
        assert count == 1
        return surv

    survey = make_survey()

    def make_question(surv):
        Question(question="first?", survey=surv).save()
        quest = Question.objects.filter().first()
        count = Question.objects.all().count()
        assert count == 1
        return quest

    question = make_question(survey)

    def add_surv_by_post():
        context = dict(title="Survey2")
        response = client.post(
                    reverse('survey_app:add_survey'), context, follow=True)
        count = Survey.objects.all().count()
        assert count == 2

    add_surv_by_post()

    def add_question_by_post(surv):
        context = dict(question="second?")
        response = client.post(reverse('survey_app:add_question',
                                kwargs={'survey_id': surv.id}),
                                context, follow=True)
        count = Question.objects.all().count()
        assert count == 2

    add_question_by_post(survey)

    def add_choice_by_post(question):
        context = dict(choice="-choice1")
        response = client.post(reverse('survey_app:add_choice',
                                kwargs={'question_id': question.id}),
                                context, follow=True)
        count = Choice.objects.all().count()
        assert count == 1

    add_choice_by_post(question)

    def resp200_survey_detail(survey):
        response = client.get(reverse('survey_app:survey_detail',
                                kwargs={'survey_id': survey.id}),
                                follow=True)
        assert response.status_code == 200

        assert b'Survey1' in response.content
        assert b'Survey2' not in response.content

    resp200_survey_detail(survey)

    def resp200_question_detail(question):
        response = client.get(reverse('survey_app:question_detail',
                                kwargs={'question_id': question.id}),
                                follow=True)
        assert response.status_code == 200

        assert b'first?' in response.content
        assert b'second?' not in response.content

    resp200_question_detail(question)
    # response = client.get(reverse('param'))

    def delete_question_by_checkbox(survey, question):
        assert Question.objects.all().count() == 2
        data = {'delete': True, str(question.id): 'on'}
        response = client.post(reverse('survey_app:survey_detail', kwargs={
                               'survey_id': survey.id}), data=data, follow=True)
        assert response.status_code == 200
        assert Question.objects.all().count() == 1

    delete_question_by_checkbox(survey, question)

    def test_registered_templates(client, param, template_name):
        # question_id = Question.objects.first().id
        survey_id = Survey.objects.first().id

        response = client.get(
            reverse(param, kwargs={'survey_id': survey_id}), follow=True)
        assert response.templates
        lst = list([t.name for t in response.templates])
        print(lst)
        lst = [x.__str__() if isinstance(x, WindowsPath) else x for x in lst]
        assert [template_name in x for x in lst]

    test_registered_templates(
        client, 'survey_app:survey_detail', 'survey_detail.html')
    test_registered_templates(
        client, 'survey_app:add_question', 'add_template.html')
    test_registered_templates(client, 'survey_app:answer', 'answer.html')

    def create_second_user(client):
        user2 = User.objects.create(username="user2", password="qwerty12542")
        client.force_login(user2)
        return user2

    user2 = create_second_user(client)

    def test_2url_list(user2):
        # response = client.get(reverse(param))
        question_id = Question.objects.first().id
        survey_id = Survey.objects.first().id

        response = client.get(reverse('survey_app:answer', kwargs={
                              'survey_id': survey.id}), follow=True)
        assert response.status_code == 200

        response = client.get(reverse('survey_app:survey_detail', kwargs={
                              'survey_id': survey.id}), follow=True)
        assert response.status_code == 404

        response = client.get(reverse('survey_app:results', kwargs={
                              'survey_id': survey.id}), follow=True)
        assert response.status_code == 404

        response = client.get(reverse('survey_app:add_question', kwargs={
                              'survey_id': survey.id}), follow=True)
        assert response.status_code == 404

        context = dict(choice="-choice1")
        response = client.post(reverse('survey_app:add_choice', kwargs={
                               'question_id': question_id}), context, follow=True)
        assert response.status_code == 404

        response = client.get(reverse('survey_app:question_detail', kwargs={
                              'question_id': question_id}), follow=True)
        assert response.status_code == 404

    test_2url_list(user2)


# @pytest.mark.parametrize(
#    'param, template_name', [
#       ('users:login_user', 'login_user.html'),
#       ('users:register', 'register.html'),
#    ]
# )
# def test_not_registered_templates(param, template_name, client):
#     # client, user = auto_login_user
#     response = client.get(reverse(param))
#     assert response.templates
#     lst = list([t.name for t in response.templates])
#     lst = [x.__str__() if isinstance(x, WindowsPath) else x for x in lst]
#     assert [template_name in x for x in lst]
