import pytest


# @pytest.mark.deb
def test_base_url_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
