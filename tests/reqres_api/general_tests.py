from collections.abc import Callable

import allure

from tests.conftest import ReqresApi
from tests.reqres_api.utils import fields_is_correct, is_almost_now, types_is_correct


class StepsSmoke:

    def __init__(self, api: ReqresApi) -> None:
        self.api = api
        self.id = 0
        self.token = None

    @allure.step("Проверка соединения.")
    def connect(self) -> None:
        assert self.api.connect(log="Проверка соединения.").status_code == 200

    @allure.step("Получение списка.")
    def get_list(self) -> None:
        response = self.api.get_list(log="Получение списка.")
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0

    @allure.step("Создание записи.")
    def create(self, data: dict) -> None:
        response = self.api.create(body=data, log="Создание записи.")
        assert response.status_code == 201
        self.id = response.json()["id"]
        assert response.json()["id"]

    @allure.step("Создание пользователя.")
    def create_user(self, user_data: dict) -> None:
        response = self.api.register(body=user_data, log="Создание пользователя.")
        assert response.status_code == 200
        assert response.json()["id"]
        self.id = response.json()["id"]
        assert response.json()["token"]

    @allure.step("Логин пользователя.")
    def login(self, user_data: dict) -> None:
        response = self.api.login(body=user_data, log="Логин пользователя.")
        assert response.status_code == 200
        self.token = response.json()["token"]
        assert self.token

    @allure.step("Получение конкретной записи.")
    def get_single(self, data: dict, field: str) -> None:
        response = self.api.get_single(id=self.id, token=self.token, log="Получение конкретной записи.")
        assert response.status_code == 200
        assert response.json()["data"][field] == data[field]

    @allure.step("Update записи.")
    def update(self, data: dict, field: str) -> None:
        response = self.api.update(id=self.id, body=data, token=self.token, log="Update записи.")
        assert response.status_code == 200
        assert response.json()[field] == data[field]

    @allure.step("Удаление записи.")
    def delete(self) -> None:
        response = self.api.inst_delete(id=self.id, token=self.token, log="Удаление записи.")
        assert response.status_code == 204


class StepsGetList:
    """Шаги проверки выдачи списка."""

    def __init__(self, api: ReqresApi) -> None:
        self.api = api
        self.user_id = None

    @allure.step("Получение списка c обычными страницами.")
    def get_correct(self, page) -> None:
        response = self.api.get_list(
            params={"page": page},
            log="Получение списка c обычными страницами.",
        )
        assert response.status_code == 200
        assert int(response.json()["page"]) == page if page != 0 else 1

    @allure.step("Получение списка c большими страницами.")
    def get_large_pages(self, page: int) -> None:
        response = self.api.get_list(params={"page": page}, log="Получение списка c большими страницами.")
        assert response.status_code == 200
        assert len(response.json()["data"]) == 0

    @allure.step("Получение списка cо страницами - строками.")
    def get_strings_pages(self, page: int) -> None:
        response = self.api.get_list(params={"page": page}, log="Получение списка cо страницами - строками.")
        assert response.status_code == 200
        assert response.json()["page"] == 1

    @allure.step("Получение списка без страницы.")
    def get_empty_page(self) -> None:
        response = self.api.get_list(log="Получение списка без страницы.")
        assert response.status_code == 200
        assert response.json()["page"] == 1

    @allure.step("Проверка типов списка.")
    def check_types(self, list_types: dict) -> None:
        response = self.api.get_list(log="Проверка типов списка.")
        assert types_is_correct(response.json(), list_types)


class StepsGetSingle:
    """Проверка выдачи конкретной записи."""

    def __init__(self, api: ReqresApi, id: int, token: str = "") -> None:
        self.api = api
        self.id = id
        self.token = token

    @allure.step("Получение корректной записи.")
    def get_correct(self) -> None:
        response = self.api.get_single(id=self.id, token=self.token, log="Получение корректной записи.")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == self.id

    @allure.step("Проверка типов ответа.")
    def check_types(self, single_types: dict) -> None:
        response = self.api.get_single(id=self.id, token=self.token, log="Проверка типов ответа.")
        assert types_is_correct(response.json()["data"], single_types)

    @allure.step("Получение c большими ID.")
    def get_big_id(self, id: int) -> None:
        response = self.api.get_single(id, token=self.token, log="Получение c большими ID.")
        assert response.status_code == 404

    @allure.step("Получение c ID - строками.")
    def get_strings_id(self, id: int) -> None:
        response = self.api.get_single(id, token=self.token, log="Получение c ID - строками.")
        assert response.status_code == 404

    @allure.step("Проверка неавторизованного доступа.")
    def unauth(self):
        response = self.api.get_single(self.id, log="Проверка неавторизованного доступа.")
        assert response.status_code == 401


class StepsCreate:
    """Проверка создания записи."""

    def __init__(self, api: ReqresApi, data: dict) -> None:
        self.api = api
        self.data = data

    @allure.step("Проверка корректной записи.")
    def create_correct(self, fields: tuple):
        response = self.api.create(body=self.data, log="Проверка корректной записи.")
        self.api.inst_delete(int(response.json()["id"]))
        assert response.status_code == 201
        assert fields_is_correct(response.json(), input=self.data, fields=fields)
        assert is_almost_now(response.json()["createdAt"][:-1])

    @allure.step("Проверка типов ответа.")
    def check_types(self, create_types: dict):
        response = self.api.create(body=self.data, log="Проверка типов ответа.")
        self.api.inst_delete(int(response.json()["id"]))
        assert types_is_correct(response.json(), create_types)

    @allure.step("Проверка пустой записи.")
    def create_empty(self):
        response = self.api.create(body=dict(), log="Проверка пустой записи.")
        self.api.inst_delete(int(response.json()["id"]))
        assert response.status_code == 400

    @allure.step("Проверка записи без обязательного поля.")
    def create_without_required(self, field: str):
        data = self.data.copy()
        data.pop(field)
        response = self.api.create(body=data, log="Проверка записи без обязательного поля.")
        self.api.inst_delete(int(response.json()["id"]))
        assert response.status_code == 400


class StepsUpdatePatch:
    """Проверка изменения записи."""

    def __init__(self, api: ReqresApi, method: Callable, id: int, token: str = "", data: dict = dict()) -> None:
        self.api = api
        self.method = method
        self.id = id
        self.token = token
        self.data = data

    @allure.step("Проверка изменения корректной записи.")
    def correct_update(self, fields: tuple):
        response = self.method(self.id, body=self.data, token=self.token, log="Проверка изменения корректной записи.")
        assert response.status_code == 200
        assert fields_is_correct(response.json(), input=self.data, fields=fields)
        assert is_almost_now(response.json()["updatedAt"][:-1])

    @allure.step("Проверка типов ответа.")
    def check_types(self, create_types: dict):
        response = self.method(self.id, body=self.data, token=self.token, log="Проверка типов ответа.")
        assert types_is_correct(response.json(), create_types)

    @allure.step("Изменение c большими ID.")
    def update_large_id(self, id: int) -> None:
        response = self.method(id, body=self.data, token=self.token, log="Изменение c большими ID.")
        assert response.status_code == 404

    @allure.step("Изменение c ID - строками.")
    def update_strings_id(self, id: int) -> None:
        response = self.method(id, body=self.data, token=self.token, log="Изменение c ID - строками.")
        assert response.status_code == 404

    @allure.step("Проверка пустой записи.")
    def update_empty(self):
        response = self.method(self.id, body=dict(), token=self.token, log="Проверка пустой записи.")
        assert response.status_code == 400

    @allure.step("Проверка обнуления обязательного поля.")
    def make_blank_required(self, field: str):
        data = self.data.copy()
        data[field] = ""
        response = self.method(self.id, body=data, token=self.token, log="Проверка обнуления обязательного поля.")
        assert response.status_code == 400

    @allure.step("Проверка неавторизованного доступа.")
    def unauth(self):
        response = self.method(self.id, body=self.data, log="Проверка неавторизованного доступа.")
        assert response.status_code == 401


class StepsRegisterLogin:
    """Проверка регистрации и логина."""

    def __init__(self, api: ReqresApi, method: Callable, data: dict) -> None:
        self.api = api
        self.method = method
        self.data = data

    @allure.step("Проверка с корректными данными.")
    def correct_entry(self):
        response = self.method(body=self.data, log="Проверка с корректными данными.")
        assert response.status_code == 200
        assert response.json()["token"]
        if self.method == self.api.register:
            assert int(response.json()["id"]) > 0

    @allure.step("Проверка типов ответа.")
    def check_types(self, correct_types: dict) -> None:
        response = self.method(body=self.data, log="Проверка типов ответа.")
        assert types_is_correct(response.json(), correct_types)

    @allure.step("Проверка без обязательного поля.")
    def entry_without_required(self, field: str):
        data = self.data.copy()
        data.pop(field)
        response = self.method(body=data, log="Проверка без обязательного поля.")
        assert response.status_code == 400

    @allure.step("Проверка с некорректным email.")
    def entry_incorrect_email(self, email: str):
        data = self.data.copy()
        data["email"] = email
        response = self.method(body=data, log="Проверка с некорректным email.")
        assert response.status_code == 400

    @allure.step("Проверка с некорректным паролем.")
    def entry_incorrect_password(self, password: str):
        data = self.data.copy()
        data["password"] = password
        response = self.method(body=data, log="Проверка с некорректным паролем.")
        assert response.status_code == 400


class StepsDelete:
    """Проверка удаления записи."""

    def __init__(self, api: ReqresApi, id: int, token: str = "") -> None:
        self.api = api
        self.id = id
        self.token = token

    @allure.step("Проверка неавторизованного удаления.")
    def unauth_delete(self):
        response = self.api.inst_delete(self.id, log="Проверка неавторизованного доступа.")
        assert response.status_code == 401

    @allure.step("Проверка авторизованного удаления.")
    def delete(self):
        response = self.api.inst_delete(self.id, token=self.token, log="Проверка неавторизованного доступа.")
        assert response.status_code == 204

    @allure.step("Получение записи.")
    def get_inst(self):
        response = self.api.get_single(self.id, token=self.token, log="Получение записи.")
        assert response.status_code == 200

    @allure.step("Получение отсутствующей записи.")
    def get_missing_inst(self):
        response = self.api.get_single(self.id, token=self.token, log="Получение отсутствующей записи.")
        assert response.status_code == 404
