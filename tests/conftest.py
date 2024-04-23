import requests
import pytest

from tests.settings import REQRES_API_URL_REGISTER, REQRES_API_URL_USERS


correct_user_data = {
    "email": "eve.holt@reqres.in",
    "password": "pistol",
    "first_name": "Eve",
    "last_name": "Holt",
    "avatar": "https://reqres.in/img/faces/4-image.jpg",
}

other_user_data = {
    "email": "michael.lawson@reqres.in",
    "first_name": "Michael",
    "last_name": "Lawson",
    "avatar": "https://reqres.in/img/faces/7-image.jpg",
}


@pytest.fixture
def correct_user():
    """
    Создание сущности пользователя в БД для использования в тесте с последующим удалением.

    Возвращает словарь с данными корректного пользователя.
    """
    response = requests.post(url=REQRES_API_URL_REGISTER, data=correct_user_data)
    id = response.json().get("id", None)
    yield {"data": correct_user_data, "id": id}
    requests.delete(url=f"{REQRES_API_URL_USERS}{id}")
