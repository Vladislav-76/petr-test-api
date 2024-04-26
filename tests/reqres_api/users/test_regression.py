import allure
from allure_commons.types import Severity

from tests.conftest import UsersApi
from tests.reqres_api.users.data import correct_user_data, other_user_data, parameters, user_list_types, user_data_types
from tests.reqres_api.utils import types_is_correct


@allure.severity(Severity.NORMAL)
def test_get_user(user_api: UsersApi) -> None:
    """Проверка получения пользователей."""

    steps = StepsGetUser(user_api)

    for page in parameters.page_digits:
        steps.step1(page)
    for page in parameters.page_large:
        steps.step2(page)
    for page in parameters.page_strings:
        steps.step3(page)
    steps.step4()
    steps.step5(correct_user_data)
    steps.step6()


class StepsGetUser:

    def __init__(self, user_api: UsersApi) -> None:
        self.api = user_api
        self.user_id = None

    @allure.step("Получение списка пользователей c обычными страницами.")
    def step1(self, page) -> None:
        response = self.api.get_list(
            params={"page": page},
            log="Получение списка пользователей c обычными страницами.",
        )
        assert response.status_code == 200
        assert int(response.json()["page"]) == page if page != 0 else 1

    @allure.step("Получение списка пользователей c большими страницами.")
    def step2(self, page) -> None:
        response = self.api.get_list(
            params={"page": page},
            log="Получение списка пользователей c большими страницами.",
        )
        assert response.status_code == 200
        assert len(response.json()["data"]) == 0

    @allure.step("Получение списка пользователей cо страницами - строками.")
    def step3(self, page) -> None:
        response = self.api.get_list(
            params={"page": page},
            log="Получение списка пользователей cо страницами - строками.",
        )
        assert response.status_code == 200
        assert response.json()["page"] == 1

    @allure.step("Получение списка пользователей без страницы.")
    def step4(self) -> None:
        response = self.api.get_list(log="Получение списка пользователей без страницы.")
        assert response.status_code == 200
        assert response.json()["page"] == 1

    @allure.step("Создание пользователя.")
    def step5(self, user_data: dict) -> None:
        response = self.api.register(body=user_data, log="Создание пользователя.")
        self.user_id = response.json()["id"]

    @allure.step("Проверка типов списка пользователей.")
    def step6(self) -> None:
        response = self.api.get_list(log="Проверка типов списка пользователей.")
        assert types_is_correct(response.json(), user_list_types)
        assert types_is_correct(response.json()["data"][0], user_data_types)

    

