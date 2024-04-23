import requests
import pytest

from tests.settings import REQRES_API_URL_REGISTER, REQRES_API_URL_USERS


correct_user_data = {
    "email": "eve.holt@reqres.in",
    "password": "pistol",
}


@pytest.fixture
def correct_user():
    response = requests.post(url=REQRES_API_URL_REGISTER, data=correct_user_data)
    yield correct_user_data
    id = response.json().get("id", None)
    requests.delete(url=f"{REQRES_API_URL_USERS}{id}")

