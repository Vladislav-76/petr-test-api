from collections.abc import Generator

import pytest
import requests
from requests import Response

from tests.settings import (REQRES_API_URL_COLORS, REQRES_API_URL_REGISTER,
                            REQRES_API_URL_USERS, Urls, USER_URLS)
from tests.reqres_api.utils import BaseApiRequest

correct_user_data: dict = {
    "id": 4,
    "email": "eve.holt@reqres.in",
    "password": "pistol",
    "first_name": "Eve",
    "last_name": "Holt",
    "avatar": "https://reqres.in/img/faces/4-image.jpg",
}

other_user_data: dict = {
    "email": "michael.lawson@reqres.in",
    "first_name": "Michael",
    "last_name": "Lawson",
    "avatar": "https://reqres.in/img/faces/7-image.jpg",
}

correct_color_data: dict = {
    "id": 2,
    "name": "fuchsia rose",
    "year": 2001,
    "color": "#C74375",
    "pantone_value": "17-2031",
}

other_color_data: dict = {
    "id": "4",
    "name": "aqua sky",
    "year": "2003",
    "color": "#7BC4C4",
    "pantone_value": "14-4811",
}


@pytest.fixture
def correct_user() -> Generator[dict, None, None]:
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
def correct_color() -> Generator[dict, None, None]:
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


class UsersApi(BaseApiRequest):
    """Класс API пользователей."""

    def __init__(self, urls: Urls) -> None:
        self.urls = urls

    def connect(self, **kwargs) -> Response:
        return self.get(url=self.urls.connect, **kwargs)

    def create(self, body: dict[str, object], **kwargs) -> Response:
        return self.post(url=self.urls.base, body=body, **kwargs)

    def register(self, body: dict[str, object], **kwargs) -> Response:
        return self.post(url=self.urls.register, body=body, **kwargs)

    def login(self, body: dict[str, object], **kwargs) -> Response:
        return self.post(url=self.urls.login, body=body, **kwargs)

    def get_list(self, **kwargs) -> Response:
        return self.get(url=self.urls.base, **kwargs)

    def get_single(self, id: int, **kwargs) -> Response:
        return self.get(url=self.urls.base + str(id), **kwargs)

    def update(self, id: int, body: dict[str, object], **kwargs) -> Response:
        return self.put(url=self.urls.base + str(id), body=body, **kwargs)

    def user_patch(self, id: int, body: dict[str, object], **kwargs) -> Response:
        return self.patch(url=self.urls.base + str(id), body=body, **kwargs)

    def user_delete(self, id: int, **kwargs) -> Response:
        return self.delete(url=self.urls.base + str(id), **kwargs)


@pytest.fixture
def user_api():
    return UsersApi(urls=USER_URLS)
