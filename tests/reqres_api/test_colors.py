import requests
import allure
import logging
from random import choice
from allure_commons.types import Severity

from tests.conftest import other_color_data
from tests.settings import REQRES_API_URL_COLORS, TEST_SUCCESS_ATTACHMENTS
from tests.reqres_api.utils import is_almost_now


@allure.severity(Severity.NORMAL)
def test_colors_list():
    """Проверка ручки LIST цветов."""

    steps = StepsList()

    steps.step1()

    params = {"page": 2, "per_page": 6}
    steps.step2(params)


class StepsList:

    @allure.step("Проверка доступности списка цветов.")
    def step1(self):
        """Проверка доступности списка цветов."""

        try:
            response = requests.get(url=REQRES_API_URL_COLORS)
            assert response.ok
            assert response.json().get("data", False)
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка доступности списка цветов завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка доступности списка цветов:\n{error}")
            raise error

    @allure.step("Проверка пагинации.")
    def step2(self, params):
        """Проверка пагинации списка цветов."""

        if requests.get(url=REQRES_API_URL_COLORS).json().get("total", 0) < params["page"] * params["per_page"]:
            allure.attach("Недостаточно записей для проверки пагинации!")
            assert True
        else:
            try:
                response = requests.get(url=REQRES_API_URL_COLORS, params=params)
                assert response.json().get("page", 0) == params["page"]
                assert len(response.json().get("data", [])) == params["per_page"]
                if TEST_SUCCESS_ATTACHMENTS:
                    allure.attach("Проверка пагинации списка цветов завершена успешно.")
            except AssertionError as error:
                logging.error(f"Ошибка пагинации списка цветов:\n{error}")
                raise error


@allure.severity(Severity.NORMAL)
def test_single_color_get(correct_color):
    """Проверка получения конкретного цвета."""

    color_data = correct_color["data"].copy()
    color_data.pop("password", None)
    color_data["id"] = correct_color["id"]
    try:
        response = requests.get(url=f"{REQRES_API_URL_COLORS}{correct_color['id']}")
        assert response.ok
        assert response.json().get("data", None) == color_data
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка получения конкретного цвета завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка получения конкретного цвета:\n{error}")
        raise error


@allure.severity(Severity.NORMAL)
def test_color_create():
    """Проверка создания цвета."""

    allure.dynamic.parameter("color_data", other_color_data)
    color_data = other_color_data.copy()
    color_data.pop("id")
    try:
        response = requests.post(url=REQRES_API_URL_COLORS, data=other_color_data)
        assert response.status_code == 201
        new_data = response.json()
        new_data.pop("id", 0)
        assert is_almost_now(new_data.pop("createdAt", None)[:-1])
        assert color_data == new_data
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка создания цвета завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка создания цвета:\n{error}")
        raise error


@allure.severity(Severity.NORMAL)
def test_user_put(correct_color):
    """Проверка PUT изменения цвета."""

    allure.dynamic.parameter("user_data", other_color_data)
    try:
        response = requests.put(url=f"{REQRES_API_URL_COLORS}{correct_color['id']}", data=other_color_data)
        assert response.ok
        new_data = response.json()
        assert is_almost_now(new_data.pop("updatedAt", None)[:-1])
        assert other_color_data == new_data
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка PUT изменения цвета завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка PUT изменения цвета:\n{error}")
        raise error


@allure.severity(Severity.NORMAL)
def test_user_patch(correct_color):
    """Проверка PATCH изменения цвета."""

    allure.dynamic.parameter("user_data", other_color_data)
    data = dict((choice(tuple(other_color_data.items())), ))
    try:
        response = requests.patch(url=f"{REQRES_API_URL_COLORS}{correct_color['id']}", data=data)
        patched_data = response.json()
        assert response.ok
        assert is_almost_now(patched_data.pop("updatedAt", None)[:-1])
        assert patched_data == data
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка PATCH изменения цвета завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка PATCH изменения цвета:\n{error}")
        raise error


@allure.severity(Severity.NORMAL)
def test_user_delete(correct_color):
    """Проверка удаления цвета."""
    try:
        response = requests.delete(url=f"{REQRES_API_URL_COLORS}{correct_color['id']}")
        assert response.status_code == 204
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка удаления цвета завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка удаления цвета:\n{error}")
        raise error
