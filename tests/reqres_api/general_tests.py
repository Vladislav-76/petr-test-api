import allure

from tests.reqres_api.utils import BaseApiRequest, types_is_correct


class StepsGetList:
    """Шаги проверки выдачи списка."""

    def __init__(self, api: BaseApiRequest) -> None:
        self.api = api
        self.user_id = None

    @allure.step("Получение списка c обычными страницами.")
    def step1(self, page) -> None:
        response = self.api.get_list(
            params={"page": page},
            log="Получение списка c обычными страницами.",
        )
        assert response.status_code == 200
        assert int(response.json()["page"]) == page if page != 0 else 1

    @allure.step("Получение списка c большими страницами.")
    def step2(self, page) -> None:
        response = self.api.get_list(params={"page": page}, log="Получение списка c большими страницами.")
        assert response.status_code == 200
        assert len(response.json()["data"]) == 0

    @allure.step("Получение списка cо страницами - строками.")
    def step3(self, page) -> None:
        response = self.api.get_list(params={"page": page}, log="Получение списка cо страницами - строками.")
        assert response.status_code == 200
        assert response.json()["page"] == 1

    @allure.step("Получение списка без страницы.")
    def step4(self) -> None:
        response = self.api.get_list(log="Получение списка без страницы.")
        assert response.status_code == 200
        assert response.json()["page"] == 1

    @allure.step("Проверка типов списка.")
    def step5(self, list_types) -> None:
        response = self.api.get_list(log="Проверка типов списка.")
        assert types_is_correct(response.json(), list_types)


class StepsGetSingle:
    """Шаги проверки выдачи конкретной сущности."""

    def __init__(self, api: BaseApiRequest, id: int, token: str = "") -> None:
        self.api = api
        self.id = id
        self.token = token

    @allure.step("Получение корректной сущности.")
    def step1(self) -> None:
        response = self.api.get_single(id=self.id, token=self.token, log="Получение корректной сущности.")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == self.id

    @allure.step("Проверка типов сущности.")
    def step2(self, single_types) -> None:
        response = self.api.get_single(id=self.id, token=self.token, log="Проверка типов ответа.")
        assert types_is_correct(response.json()["data"], single_types)

    @allure.step("Получение c большими ID.")
    def step3(self, id) -> None:
        response = self.api.get_single(id, token=self.token, log="Получение c большими ID.")
        assert response.status_code == 404

    @allure.step("Получение c ID - строками.")
    def step4(self, id) -> None:
        response = self.api.get_single(id, token=self.token, log="Получение c ID - строками.")
        assert response.status_code == 404

