import allure
from allure_commons.types import Severity

from tests.conftest import ReqresApi
from tests.reqres_api.colors.data import correct_color_data, other_color_data
from tests.reqres_api.general_tests import StepsSmoke


@allure.severity(Severity.CRITICAL)
def test_smoke(colors_api: ReqresApi) -> None:
    """Проверка основной функциональности."""

    steps = StepsSmoke(colors_api)

    steps.connect()
    steps.get_list()
    steps.create(correct_color_data)
    steps.get_single(correct_color_data, field="name")
    steps.update(other_color_data, field="color")
    steps.delete()
