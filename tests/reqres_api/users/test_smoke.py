import allure
from allure_commons.types import Severity

from tests.conftest import ReqresApi
from tests.reqres_api.general_tests import StepsSmoke
from tests.reqres_api.users.data import correct_user_data, other_user_data


@allure.severity(Severity.CRITICAL)
def test_smoke(users_api: ReqresApi) -> None:
    """Проверка основной функциональности."""

    steps = StepsSmoke(users_api)

    steps.connect()
    steps.get_list()
    steps.create_user(correct_user_data)
    steps.login(correct_user_data)
    steps.get_single(correct_user_data, field="email")
    steps.update(other_user_data, field="first_name")
    steps.delete()
