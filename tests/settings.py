from collections import namedtuple


BASE_URL: str = "https://reqres.in/api/"
# REQRES_API_URL_CHECK: str = f"{BASE_URL}smth/"
# REQRES_API_URL_COLORS: str = f"{BASE_URL}colors/"
# REQRES_API_URL_LOGIN: str = f"{BASE_URL}login/"
# REQRES_API_URL_LOGOUT: str = f"{BASE_URL}logout/"
# REQRES_API_URL_REGISTER: str = f"{BASE_URL}register/"
# REQRES_API_URL_USERS: str = f"{BASE_URL}users/"

# TEST_SUCCESS_ATTACHMENTS: bool = True

Urls = namedtuple("Urls", ("connect", "login", "logout", "register", "base"))

USER_URLS = Urls(connect="smth/", login="login/", logout="logout/", register="register/", base="users/")
