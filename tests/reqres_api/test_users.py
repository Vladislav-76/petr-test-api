import logging
from random import choice

import allure
import requests
from allure_commons.types import Severity

from tests.conftest import correct_user_data, other_user_data
from tests.reqres_api.utils import is_almost_now
from tests.settings import (REQRES_API_URL_REGISTER, REQRES_API_URL_USERS,
                            TEST_SUCCESS_ATTACHMENTS)


@allure.severity(Severity.NORMAL)
def test_users_list():
    """Проверка ручки LIST пользователей."""

    steps = StepsList()

    steps.step1()

    params = {"page": 2, "per_page": 6}
    steps.step2(params)


class StepsList:

    @allure.step("Проверка доступности списка пользователей.")
    def step1(self):
        """Проверка доступности списка пользователей."""

        try:
            response = requests.get(url=REQRES_API_URL_USERS)
            assert response.ok
            assert response.json().get("data", False)
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка доступности списка пользователей завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка доступности списка пользователей:\n{error}")
            raise error

    @allure.step("Проверка пагинации.")
    def step2(self, params):
        """Проверка пагинации списка пользователей."""

        if requests.get(url=REQRES_API_URL_USERS).json().get("total", 0) < params["page"] * params["per_page"]:
            allure.attach("Недостаточно записей для проверки пагинации!")
            assert True
        else:
            try:
                response = requests.get(url=REQRES_API_URL_USERS, params=params)
                assert response.json().get("page", 0) == params["page"]
                assert len(response.json().get("data", [])) == params["per_page"]
                if TEST_SUCCESS_ATTACHMENTS:
                    allure.attach("Проверка пагинации списка пользователей завершена успешно.")
            except AssertionError as error:
                logging.error(f"Ошибка пагинации списка пользователей:\n{error}")
                raise error


@allure.severity(Severity.NORMAL)
def test_single_user_get(correct_user):
    """Проверка получения конкретного пользователя."""

    user_data = correct_user["data"].copy()
    user_data.pop("password", None)
    user_data["id"] = correct_user["id"]
    try:
        response = requests.get(url=f"{REQRES_API_URL_USERS}{correct_user['id']}")
        assert response.ok
        assert response.json().get("data", None) == user_data
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка получения конкретного пользователя завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка получения конкретного пользователя:\n{error}")
        raise error


@allure.severity(Severity.NORMAL)
def test_user_register():
    """Проверка создания пользователя."""

    steps = StepsRegister()

    steps.step1(correct_user_data)

    user_password_out = correct_user_data.copy()
    user_password_out.pop("password", None)
    steps.step2(user_password_out)

    user_email_out = correct_user_data.copy()
    user_email_out.pop("email", None)
    steps.step3(user_email_out)


class StepsRegister:

    @allure.step("Проверка создания корректного пользователя.")
    def step1(self, correct_user_data):
        """Проверка создания корректного пользователя."""

        try:
            response = requests.post(url=REQRES_API_URL_REGISTER, data=correct_user_data)
            assert response.status_code == 200
            assert response.json().get("id", False) and response.json().get("token", False)
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка создания корректного пользователя завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка создания корректного пользователя:\n{error}")
            raise error

    @allure.step("Проверка создания пользователя без пароля.")
    def step2(self, user_password_out):
        """Проверка создания пользователя без пароля."""

        try:
            response = requests.post(url=REQRES_API_URL_REGISTER, data=user_password_out)
            assert response.status_code == 400
            assert response.json().get("error", False)
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка создания пользователя без пароля завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка создания пользователя без пароля:\n{error}")
            raise error

    @allure.step("Проверка создания пользователя без почты.")
    def step3(self, user_email_out):
        """Проверка создания пользователя без почты."""

        try:
            response = requests.post(url=REQRES_API_URL_REGISTER, data=user_email_out)
            assert response.status_code == 400
            assert response.json().get("error", False)
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка создания пользователя без почты завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка создания пользователя без почты:\n{error}")
            raise error


@allure.severity(Severity.NORMAL)
def test_user_put(correct_user):
    """Проверка PUT изменения пользователя."""

    allure.dynamic.parameter("user_data", other_user_data)
    try:
        response = requests.put(url=f"{REQRES_API_URL_USERS}{correct_user['id']}", data=other_user_data)
        assert response.ok
        user_data = response.json()
        assert is_almost_now(user_data.pop("updatedAt", None)[:-1])
        assert user_data == other_user_data
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка PUT изменения пользователя завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка PUT изменения пользователя:\n{error}")
        raise error


@allure.severity(Severity.NORMAL)
def test_user_patch(correct_user):
    """Проверка PATCH изменения пользователя."""

    allure.dynamic.parameter("user_data", other_user_data)
    data = dict((choice(tuple(other_user_data.items())), ))
    try:
        response = requests.patch(url=f"{REQRES_API_URL_USERS}{correct_user['id']}", data=data)
        patched_data = response.json()
        assert response.ok
        assert is_almost_now(patched_data.pop("updatedAt", None)[:-1])
        assert patched_data == data
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка PATCH изменения пользователя завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка PATCH изменения пользователя:\n{error}")
        raise error


@allure.severity(Severity.NORMAL)
def test_user_delete(correct_user):
    """Проверка удаления пользователя."""
    try:
        response = requests.delete(url=f"{REQRES_API_URL_USERS}{correct_user['id']}")
        assert response.status_code == 204
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка удаления пользователя завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка удаления пользователя:\n{error}")
        raise error
