from pathlib import WindowsPath

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "param",
    [
        "survey_app:home",
        "survey_app:surveys_to_pass",
        "survey_app:register",
        "survey_app:login",
    ],
)
def test_get200_request(param, client):
    """access without auto_login_user"""
    response = client.get(reverse(param), follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "param",
    [
        "survey_app:add_survey",
        "survey_app:register",
        "survey_app:login",
        "survey_app:survey_list",
    ],
)
def test_url_list(param, auto_login_user):
    """access with auto_login_user"""
    client, user = auto_login_user
    response = client.get(reverse(param))
    assert response.status_code == 200


@pytest.mark.parametrize(
    "param, template_name",
    [
        ("survey_app:login", "login.html"),
        ("survey_app:register", "register.html"),
    ],
)
def test_not_registered_templates(param, template_name, client):
    response = client.get(reverse(param))
    assert response.templates
    lst = list([t.name for t in response.templates])
    lst = [x.__str__() if isinstance(x, WindowsPath) else x for x in lst]
    opts = [x for x in lst]
    assert template_name in opts
