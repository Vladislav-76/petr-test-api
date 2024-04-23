import requests
import allure
import logging
from allure_commons.types import Severity

from tests.settings import REQRES_API_URL_LOGIN, REQRES_API_URL_LOGOUT, TEST_SUCCESS_ATTACHMENTS


@allure.severity(Severity.CRITICAL)
def test_login(correct_user):
    """Проверка ручки login."""

    steps = StepsAuth()

    steps.step1(correct_user["data"])

    incorrect_user = correct_user["data"].copy()
    incorrect_user["email"] = "incorrect_email"
    steps.step2(incorrect_user)

    user_password_out = correct_user["data"].copy()
    user_password_out.pop("password", None)
    steps.step3(user_password_out)


class StepsAuth:

    @allure.step("Логин корректного пользователя.")
    def step1(self, correct_user):
        """Проверка login с корректными данными."""

        try:
            response = requests.post(url=REQRES_API_URL_LOGIN, data=correct_user)
            assert response.ok
            assert response.json().get("token", False)
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка login с корректными данными завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка login с корректными данными:\n{error}")
            raise error

    @allure.step("Логин некорректного пользователя.")
    def step2(self, incorrect_user):
        """Проверка login с некорректными данными."""

        try:
            response = requests.post(url=REQRES_API_URL_LOGIN, data=incorrect_user)
            assert response.status_code == 400
            assert response.json().get("token", False) is False
            assert response.json().get("error", False)
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка login с некорректными данными завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка login с некорректными данными:\n{error}")
            raise error

    @allure.step("Логин без пароля.")
    def step3(self, user_password_out):
        """Проверка login без пароля."""

        try:
            response = requests.post(url=REQRES_API_URL_LOGIN, data=user_password_out)
            assert response.status_code == 400
            assert response.json().get("token", False) is False
            assert response.json().get("error", False)
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка login без пароля завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка login без пароля:\n{error}")
            raise error


@allure.severity(Severity.NORMAL)
def test_logout():
    """Проверка ручки logout."""

    try:
        assert requests.post(REQRES_API_URL_LOGOUT).status_code == 200
        if TEST_SUCCESS_ATTACHMENTS:
            allure.attach("Проверка logout завершена успешно.")
    except AssertionError as error:
        logging.error(f"Ошибка logout:\n{error}")
        raise error
