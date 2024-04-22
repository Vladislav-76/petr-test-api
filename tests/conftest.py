import requests
import allure
import pytest
import logging

from settings import REQRES_API_URL_REGISTER


correct_user = {
    "username": "correct_user",
    "email": "correct_user@mail.com",
    "password": "correct_password",
}

@pytest.fixture
def test_user():
    response = requests.post(url=REQRES_API_URL_REGISTER, data=correct_user)
    yield response
    requests.delete

