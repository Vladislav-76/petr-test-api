import allure
from allure_commons.types import Severity

from tests.conftest import ReqresApi
from tests.reqres_api.general_tests import (
    StepsCreate, StepsUpdatePatch, StepsGetList, StepsGetSingle, StepsRegisterLogin)
from tests.reqres_api.users.data import correct_user_data, parameters, user_list_types, user_data_types


@allure.severity(Severity.NORMAL)
def test_get_user_list(user_api: ReqresApi) -> None:
    """Проверка получения списка пользователей."""

    steps = StepsGetList(user_api)

    for page in parameters.page_digits:
        steps.get_correct(page)
    for page in parameters.large_digits:
        steps.get_large_pages(page)
    for page in parameters.strings:
        steps.get_strings_pages(page)
    steps.get_empty_page()
    steps.check_types(user_list_types)


@allure.severity(Severity.NORMAL)
def test_get_single_user(user_api: ReqresApi, auth_user_create: callable) -> None:
    """Проверка получения конкретного пользователя."""

    id, token = auth_user_create
    steps = StepsGetSingle(user_api, id, token)

    steps.get_correct()
    steps.check_types(user_data_types)
    for id in parameters.large_digits:
        steps.get_big_id(id)
    for id in parameters.strings:
        steps.get_strings_id(id)
    steps.unauth()


@allure.severity(Severity.NORMAL)
def test_create_user(user_api: ReqresApi) -> None:
    """Проверка создания пользователя."""

    steps = StepsCreate(user_api, correct_user_data)

    steps.create_correct(fields=parameters.user_fields)
    steps.check_types(user_data_types)
    steps.create_empty()
    for field in parameters.user_required_fields:
        steps.create_without_required(field)


@allure.severity(Severity.NORMAL)
def test_update_user(user_api: ReqresApi, auth_user_create: callable) -> None:
    """Проверка изменения пользователя."""

    id, token = auth_user_create
    steps = StepsUpdatePatch(user_api, user_api.update, id, token, correct_user_data)

    steps.correct_update(fields=parameters.user_fields)
    steps.check_types(user_data_types)
    for id in parameters.large_digits:
        steps.update_large_id(id)
    for id in parameters.strings:
        steps.update_strings_id(id)
    steps.update_empty()
    for field in parameters.user_required_fields:
        steps.make_blank_required(field)
    steps.unauth()


@allure.severity(Severity.NORMAL)
def test_patch_user(user_api: ReqresApi, auth_user_create: callable) -> None:
    """Проверка Patch пользователя."""

    id, token = auth_user_create
    steps = StepsUpdatePatch(user_api, user_api.inst_patch, id, token, correct_user_data)

    steps.correct_update(fields=parameters.user_fields)
    steps.check_types(user_data_types)
    for id in parameters.large_digits:
        steps.update_large_id(id)
    for id in parameters.strings:
        steps.update_strings_id(id)
    steps.update_empty()
    for field in parameters.user_required_fields:
        steps.make_blank_required(field)
    steps.unauth()


@allure.severity(Severity.NORMAL)
def test_register(user_api: ReqresApi) -> None:
    """Проверка регистрации."""

    steps = StepsRegisterLogin(user_api, user_api.register, correct_user_data)

    steps.correct_entry()
    steps.check_types(user_data_types)
    for field in parameters.user_required_fields:
        steps.entry_without_required(field)
    for email in parameters.incorrect_emails:
        steps.entry_incorrect_email(email)
    for password in parameters.incorrect_passwords:
        steps.entry_incorrect_password(password)


@allure.severity(Severity.NORMAL)
def test_login(user_api: ReqresApi) -> None:
    """Проверка логина."""

    steps = StepsRegisterLogin(user_api, user_api.login, correct_user_data)

    steps.correct_entry()
    steps.check_types(user_data_types)
    for field in parameters.user_required_fields:
        steps.entry_without_required(field)
    for email in parameters.incorrect_emails:
        steps.entry_incorrect_email(email)
    for password in parameters.incorrect_passwords:
        steps.entry_incorrect_password(password)
