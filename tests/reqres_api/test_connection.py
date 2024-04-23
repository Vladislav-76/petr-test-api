import logging

import allure
import requests
from allure_commons.types import Severity

from tests.settings import (REQRES_API_URL_CHECK, REQRES_API_URL_USERS,
                            TEST_SUCCESS_ATTACHMENTS)


@allure.severity(Severity.BLOCKER)
def test_connection():
    """
    Проверка подключений к API.

    - проверяется возможность подключения;
    - проверяется подключение с задержкой ответа.
    """

    steps = StepsConnection()

    steps.step1()
    steps.step2()


class StepsConnection:

    @allure.step("Проверка статуса подключения.")
    def step1(self):
        """Проверка подключения к reqres.in/api/"""

        try:
            assert requests.get(url=REQRES_API_URL_CHECK).status_code == 200
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка подключения к reqres.in/api/ завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка при подключении к {REQRES_API_URL_CHECK}:\n{error}")
            raise error

    @allure.step("Задержка подключения.")
    def step2(self):
        """Проверка подключения c задержкой."""

        allure.dynamic.parameter("delay", 3)
        response = requests.get(url=REQRES_API_URL_USERS, params={"delay": 3})
        try:
            assert response.status_code == 200
            assert len(response.json()["data"]) > 0
            if TEST_SUCCESS_ATTACHMENTS:
                allure.attach("Проверка подключения c задержкой завершена успешно.")
        except AssertionError as error:
            logging.error(f"Ошибка при подключении c задержкой к {REQRES_API_URL_USERS}:\n{error}")
            raise error
