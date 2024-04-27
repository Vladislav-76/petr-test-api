import allure
from allure_commons.types import Severity

from tests.conftest import UsersApi
from tests.reqres_api.general_tests import StepsGetList, StepsGetSingle
from tests.reqres_api.users.data import correct_user_data, other_user_data, parameters, user_list_types, user_data_types
from tests.reqres_api.utils import types_is_correct


@allure.severity(Severity.NORMAL)
def test_get_user_list(user_api: UsersApi) -> None:
    """Проверка получения списка пользователей."""

    steps = StepsGetList(user_api)

    for page in parameters.page_digits:
        steps.step1(page)
    for page in parameters.large_digits:
        steps.step2(page)
    for page in parameters.strings:
        steps.step3(page)
    steps.step4()
    steps.step5(user_list_types)


@allure.severity(Severity.NORMAL)
def test_get_single_user(user_api: UsersApi, auth_user_create: callable) -> None:
    """Проверка получения конкретного пользователя."""

    id, token = auth_user_create
    steps = StepsGetSingle(user_api, id, token)

    steps.step1()
    steps.step2(user_data_types)
    for id in parameters.large_digits:
        steps.step3(id)
    for id in parameters.strings:
        steps.step4(id)

    

