import logging

import pytest

from survey_app.models import Choice, Question, Survey, User
from survey_app.tests.utils import (
    add_choice_by_post,
    add_question_by_post,
    add_survey_by_post,
    check_registered_templates,
    create_second_user,
    delete_question_by_checkbox,
    get_response_from_url_with_follow,
    make_question,
    make_survey,
    resp200_question_detail,
    resp200_survey_detail,
)

logger = logging.getLogger(__name__)


def test_user(auto_login_user, db):
    count = User.objects.all().count()
    assert count == 1


def test_pages_with_db(auto_login_user, client, db):
    user = auto_login_user

    survey = make_survey(user)
    count = Survey.objects.all().count()
    assert count == 1

    question = make_question(survey)
    count = Question.objects.all().count()
    assert count == 1

    response = add_survey_by_post(client)
    assert response.status_code == 200
    count = Survey.objects.all().count()
    assert count == 2

    response = add_question_by_post(survey, client)
    assert response.status_code == 200
    count = Question.objects.all().count()
    assert count == 2

    response = add_choice_by_post(question, client)
    assert response.status_code == 200
    count = Choice.objects.all().count()
    assert count == 1

    response = resp200_survey_detail(survey, client)
    assert response.status_code == 200
    assert b"Survey1" in response.content
    assert b"Survey2" not in response.content

    response = resp200_question_detail(question, client)
    assert response.status_code == 200
    assert b"first?" in response.content
    assert b"second?" not in response.content

    response = delete_question_by_checkbox(survey, question, client)
    assert response.status_code == 200
    assert Question.objects.all().count() == 1

    response, temps = check_registered_templates(client, "survey_app:survey_detail")
    assert "survey_detail.html" in temps

    response, temps = check_registered_templates(client, "survey_app:add_question")
    assert "add_template.html" in temps

    response, temps = check_registered_templates(client, "survey_app:answer")
    # <QuerySet []>
    assert "answer.html" in temps

    user2 = create_second_user(client)
    question_id = Question.objects.first().id
    survey_id = Survey.objects.first().id
    assert question_id
    assert survey_id

    response = get_response_from_url_with_follow(
        client, "survey_app:answer", {"survey_id": survey.id}
    )
    assert response.status_code == 200

    response = get_response_from_url_with_follow(
        client, "survey_app:survey_detail", {"survey_id": survey.id}
    )
    assert response.status_code == 404

    response = get_response_from_url_with_follow(
        client, "survey_app:results", {"survey_id": survey.id}
    )
    assert response.status_code == 404

    response = get_response_from_url_with_follow(
        client, "survey_app:add_question", {"survey_id": survey.id}
    )
    assert response.status_code == 404

    response = get_response_from_url_with_follow(
        client,
        "survey_app:add_choice",
        {"question_id": question_id},
        context=dict(choice="-choice1"),
    )
    assert response.status_code == 404

    response = get_response_from_url_with_follow(
        client, "survey_app:question_detail", {"question_id": question_id}
    )
    assert response.status_code == 404
