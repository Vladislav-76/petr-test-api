from collections import namedtuple

BASE_URL: str = "https://reqres.in/api/"

Urls = namedtuple("Urls", ("connect", "login", "logout", "register", "base"), defaults=("", "", "", "", ""))

USER_URLS = Urls(connect="connect/", login="login/", logout="logout/", register="register/", base="users/")
COLORS_URLS = Urls(connect="connect/", base="colors/")
