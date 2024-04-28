from collections.abc import Generator

import pytest
from requests import Response

from tests.reqres_api.colors.data import correct_color_data
from tests.reqres_api.users.data import correct_user_data
from tests.reqres_api.utils import BaseApiRequest
from tests.settings import COLORS_URLS, USER_URLS, Urls


class ReqresApi(BaseApiRequest):
    """Класс API пользователей."""

    def __init__(self, urls: Urls) -> None:
        self.urls = urls

    def connect(self, **kwargs) -> Response:
        return self.get(url=self.urls.connect, **kwargs)

    def create(self, body: dict[str, object], **kwargs) -> Response:
        return self.post(url=self.urls.base, body=body, **kwargs)

    def register(self, body: dict[str, object], **kwargs) -> Response:
        return self.post(url=self.urls.register, body=body, **kwargs)

    def login(self, body: dict[str, object], **kwargs) -> Response:
        return self.post(url=self.urls.login, body=body, **kwargs)

    def get_list(self, **kwargs) -> Response:
        return self.get(url=self.urls.base, **kwargs)

    def get_single(self, id: int, **kwargs) -> Response:
        return self.get(url=self.urls.base + str(id), **kwargs)

    def update(self, id: int, body: dict[str, object], **kwargs) -> Response:
        return self.put(url=self.urls.base + str(id), body=body, **kwargs)

    def inst_patch(self, id: int, body: dict[str, object], **kwargs) -> Response:
        return self.patch(url=self.urls.base + str(id), body=body, **kwargs)

    def inst_delete(self, id: int, **kwargs) -> Response:
        return self.delete(url=self.urls.base + str(id), **kwargs)


@pytest.fixture
def users_api() -> ReqresApi:
    return ReqresApi(USER_URLS)


@pytest.fixture
def colors_api() -> ReqresApi:
    return ReqresApi(COLORS_URLS)


@pytest.fixture
def auth_user_create() -> Generator[tuple[int, str], None, None]:
    api = ReqresApi(USER_URLS)
    id = api.register(correct_user_data).json()["id"]
    token = api.login(correct_user_data).json()["token"]
    yield id, token
    api.inst_delete(id)


@pytest.fixture
def color_create() -> Generator[int, None, None]:
    api = ReqresApi(COLORS_URLS)
    id = api.create(correct_color_data).json()["id"]
    yield id
    api.inst_delete(id)
