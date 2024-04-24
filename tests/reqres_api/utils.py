from datetime import datetime, timedelta

import allure

from tests.settings import TEST_SUCCESS_ATTACHMENTS


def attach_to_allure_report(text: str) -> None:
    if TEST_SUCCESS_ATTACHMENTS:
        allure.attach(text)


def is_almost_now(iso_time: str) -> bool:
    iso_time = datetime.fromisoformat(iso_time)
    time_now = datetime.now(tz=iso_time.tzinfo)
    return iso_time > time_now - timedelta(minutes=5)
