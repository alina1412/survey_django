import pytest
from django.contrib.auth.models import User

from survey_app.models import User


def auto_create_user(db):
    user = User.objects.create(username="user1", password="qwerty12542")
    return user


# pytest-django has a build-in fixture client and db
@pytest.fixture(scope="function")
def auto_login_user(client, db):
    user = auto_create_user(db)
    client.force_login(user)
    return user
