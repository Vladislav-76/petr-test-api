import allure
from allure_commons.types import Severity

from tests.conftest import UsersApi
from tests.reqres_api.users.data import correct_user_data, other_user_data


@allure.severity(Severity.CRITICAL)
def test_smoke(user_api: UsersApi) -> None:
    """Проверка основной функциональности."""

    steps = StepsSmoke(user_api)

    steps.step1()
    steps.step2()
    steps.step3(correct_user_data)
    steps.step4(correct_user_data)
    steps.step5(correct_user_data)
    steps.step6(other_user_data)
    steps.step7()


class StepsSmoke:

    def __init__(self, user_api: UsersApi) -> None:
        self.api = user_api
        self.user_id = None

    @allure.step("Проверка соединения.")
    def step1(self) -> None:
        assert self.api.connect(log="Проверка соединения.").status_code == 200

    @allure.step("Получение списка пользователей.")
    def step2(self) -> None:
        response = self.api.get_list(log="Получение списка пользователей.")
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0

    @allure.step("Создание пользователя.")
    def step3(self, user_data: dict) -> None:
        response = self.api.register(body=user_data, log="Создание пользователя.")
        assert response.status_code == 200
        assert response.json()["id"]
        self.user_id = response.json()["id"]
        assert response.json()["token"]

    @allure.step("Логин пользователя.")
    def step4(self, user_data: dict) -> None:
        response = self.api.login(body=user_data, log="Логин пользователя.")
        assert response.status_code == 200
        assert response.json()["token"]

    @allure.step("Получение конкретного пользователя.")
    def step5(self, user_data: dict) -> None:
        response = self.api.get_single(id=self.user_id, log="Получение конкретного пользователя.")
        assert response.status_code == 200
        assert response.json()["data"]["email"] == user_data["email"]

    @allure.step("Update пользователя.")
    def step6(self, user_data: dict) -> None:
        response = self.api.update(id=self.user_id, body=user_data, log="Update пользователя.")
        assert response.status_code == 200
        assert response.json()["first_name"] == user_data["first_name"]

    @allure.step("Удаление пользователя.")
    def step7(self) -> None:
        response = self.api.user_delete(id=self.user_id, log="Удаление пользователя.")
        assert response.status_code == 204
