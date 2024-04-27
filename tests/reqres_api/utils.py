from datetime import datetime, timedelta
from textwrap import dedent

import allure
import requests
from requests import Response

# from tests.settings import TEST_SUCCESS_ATTACHMENTS


# def attach_to_allure_report(text: str) -> None:
#     if TEST_SUCCESS_ATTACHMENTS:
#         allure.attach(text)


def is_almost_now(iso_time: str) -> bool:
    iso_time = datetime.fromisoformat(iso_time)
    time_now = datetime.now(tz=iso_time.tzinfo)
    return iso_time > time_now - timedelta(minutes=5)


def types_is_correct(response: dict, model: dict) -> str:
    return all(isinstance(value, model[key]) for key, value in response.items())


def fields_is_correct(response: dict, input: dict, fields: tuple):
    return all(response.get(field) == input.get(field) for field in fields)


class BaseApiRequest:
    """Базовый класс запросов к API."""

    base_url: str = "https://reqres.in/api/"
    headers: dict = {"Content-Type": "application/json"}
    cookies: str = ""
    timeout: int = 5

    def base_request(self, method: str, url: str, **kwargs) -> Response:
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            cookies=self.cookies,
            params=kwargs.get("params", None),
            json=kwargs.get("body", None),
            timeout=self.timeout,
        )
        if "log" in kwargs:
            allure.attach(body=self.make_log(response), name=kwargs["log"])
        return response

    @staticmethod
    def make_log(response: Response) -> str:
        return dedent(
            f"""
            REQUEST:
            URL: {response.request.url}
            METHOD: {response.request.method}
            HEADERS: {response.request.headers}
            BODY: {response.request.body}

            RESPONSE:
            STATUS_CODE: {response.status_code}
            DATA: {response.text}
        """
        )

    # def auth(self, auth_url: str, user: str, password: str, **kwargs) -> Response:
    #     return self.base_request(method="POST", url=self.base_url + auth_url, auth=(user, password), **kwargs)

    def get(self, url: str, **kwargs) -> Response:
        return self.base_request(method="GET", url=self.base_url + url, **kwargs)

    def post(self, url: str, body: dict[str, object], **kwargs) -> Response:
        return self.base_request(method="POST", url=self.base_url + url, body=body, **kwargs)

    def put(self, url: str, body: dict[str, object], **kwargs) -> Response:
        return self.base_request(method="PUT", url=self.base_url + url, body=body, **kwargs)

    def patch(self, url: str, body: dict[str, object], **kwargs) -> Response:
        return self.base_request(method="PATCH", url=self.base_url + url, body=body, **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        return self.base_request(method="DELETE", url=self.base_url + url, **kwargs)
