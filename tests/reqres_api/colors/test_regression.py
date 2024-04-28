import allure
from allure_commons.types import Severity

from tests.conftest import ReqresApi
from tests.reqres_api.colors.data import color_data_types, color_list_types, correct_color_data, parameters
from tests.reqres_api.general_tests import StepsCreate, StepsDelete, StepsGetList, StepsGetSingle, StepsUpdatePatch


@allure.severity(Severity.NORMAL)
def test_get_colors_list(colors_api: ReqresApi) -> None:
    """Проверка получения списка цветов."""

    steps = StepsGetList(colors_api)

    for page in parameters.page_digits:
        steps.get_correct(page)
    for page in parameters.large_digits:
        steps.get_large_pages(page)
    for page in parameters.strings:
        steps.get_strings_pages(page)
    steps.get_empty_page()
    steps.check_types(color_list_types)


@allure.severity(Severity.NORMAL)
def test_get_single_color(colors_api: ReqresApi, color_create: int) -> None:
    """Проверка получения конкретного цвета."""

    id = color_create
    steps = StepsGetSingle(colors_api, id)

    steps.get_correct()
    steps.check_types(color_data_types)
    for id in parameters.large_digits:
        steps.get_big_id(id)
    for id in parameters.strings:
        steps.get_strings_id(id)


@allure.severity(Severity.NORMAL)
def test_create_color(colors_api: ReqresApi) -> None:
    """Проверка создания цвета."""

    steps = StepsCreate(colors_api, correct_color_data)

    steps.create_correct(fields=parameters.color_fields)
    steps.check_types(color_data_types)
    steps.create_empty()


@allure.severity(Severity.NORMAL)
def test_update_color(colors_api: ReqresApi, color_create: int) -> None:
    """Проверка изменения цвета."""

    id = color_create
    steps = StepsUpdatePatch(colors_api, method=colors_api.update, id=id, data=correct_color_data)

    steps.correct_update(fields=parameters.color_fields)
    steps.check_types(color_data_types)
    for id in parameters.large_digits:
        steps.update_large_id(id)
    for id in parameters.strings:
        steps.update_strings_id(id)
    steps.update_empty()


@allure.severity(Severity.NORMAL)
def test_patch_color(colors_api: ReqresApi, color_create: int) -> None:
    """Проверка Patch цвета."""

    id = color_create
    steps = StepsUpdatePatch(colors_api, method=colors_api.inst_patch, id=id, data=correct_color_data)

    steps.correct_update(fields=parameters.color_fields)
    steps.check_types(color_data_types)
    for id in parameters.large_digits:
        steps.update_large_id(id)
    for id in parameters.strings:
        steps.update_strings_id(id)
    steps.update_empty()


@allure.severity(Severity.NORMAL)
def test_delete_color(colors_api: ReqresApi, color_create: int) -> None:
    """Проверка удаления цвета."""

    id = color_create
    steps = StepsDelete(colors_api, id=id)

    steps.delete()
    steps.get_missing_inst()
