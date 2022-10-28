import pytest

from survey_app.models import User


# pytest-django has a build-in fixture client
@pytest.fixture()
def auto_login_user(db, client):
    print()
    print("fixture\n")
    user = User.objects.create(username="user1", password="qwerty12542")
    client.force_login(user)
    return client, user
