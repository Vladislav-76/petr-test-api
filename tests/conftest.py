import pytest
import requests

from tests.settings import (REQRES_API_URL_COLORS, REQRES_API_URL_REGISTER,
                            REQRES_API_URL_USERS)

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

correct_color_data = {
    "id": 2,
    "name": "fuchsia rose",
    "year": 2001,
    "color": "#C74375",
    "pantone_value": "17-2031",
}

other_color_data = {
    "id": "4",
    "name": "aqua sky",
    "year": "2003",
    "color": "#7BC4C4",
    "pantone_value": "14-4811",
}


@pytest.fixture
def correct_user():
    """
    Создание сущности пользователя в БД для использования в тесте с последующим удалением.

    Возвращает словарь с данными корректного пользователя.
    """

    # На самом деле API не позволяет ничего создать, но возвращает в ответе уже созданного пользователя

    response = requests.post(url=REQRES_API_URL_REGISTER, data=correct_user_data)
    id = response.json().get("id", None)
    yield {"data": correct_user_data, "id": id}
    requests.delete(url=f"{REQRES_API_URL_USERS}{id}")


@pytest.fixture
def correct_color():
    """
    Создание сущности цвета в БД для использования в тесте с последующим удалением.

    Возвращает словарь с данными корректного цвета.
    """

    # На самом деле API только делает вид, что создает новую запись
    # По возвращаемому от API id ничего не получить

    response = requests.post(url=REQRES_API_URL_COLORS, data=correct_color_data)
    id = response.json().get("id", None)
    yield {"data": correct_color_data, "id": correct_color_data["id"]}  # Поэтому берем id из нашей даты
    requests.delete(url=f"{REQRES_API_URL_COLORS}{id}")
