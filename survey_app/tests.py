
from pathlib import WindowsPath
from django.test import SimpleTestCase, TestCase, Client
from django import urls
import pytest

import logging
logger = logging.getLogger(__name__)

from .views import *
from .models import *


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


@pytest.mark.parametrize(
        'param', [
            '/survey/create/',
            '/survey/list/',
            '/survey/'
        ]
    )
def test_get200_request(param, client):
   response = client.get(param, follow=True)
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
   

# @pytest.mark.django_db
# def test_books_list(auto_login_user):
#     client, user = auto_login_user
#     response = client.get('/shelves/table_books/')
#     assert response.status_code == 200
#     assert b'table of books' in response.content
#     assert b'example_author_' in response.content


# @pytest.mark.parametrize(
#    'param, template_name', [
#       ('shelves:books_add', 'books_add.html'),
#       ('shelves:table_books', 'list_draft.html'),
#       ('shelves:book_search', 'query.html'),
#    ]
# )
# def test_registered_templates(param, template_name, client, auto_login_user):
#     client, user = auto_login_user
#     response = client.get(reverse(param))
#     assert response.templates
#     lst = list([t.name for t in response.templates])
#     print(lst)
#     lst = [x.__str__() if isinstance(x, WindowsPath) else x for x in lst]
#     assert [template_name in x for x in lst]


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

