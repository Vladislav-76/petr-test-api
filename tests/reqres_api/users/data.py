from collections import namedtuple

correct_user_data: dict = {
    "email": "eve.holt@reqres.in",
    "password": "pistol",
    "name": "Eve",
    "first_name": "Eve",
    "last_name": "Holt",
    "avatar": "https://reqres.in/img/faces/4-image.jpg",
}

other_user_data: dict = {
    "email": "michael.lawson@reqres.in",
    "first_name": "Michael",
    "last_name": "Lawson",
    "avatar": "https://reqres.in/img/faces/7-image.jpg",
}

user_data_types: dict = {
    "id": int,
    "email": str,
    "password": str,
    "name": str,
    "first_name": str,
    "last_name": str,
    "avatar": str,
    "createdAt": str,
    "updatedAt": str,
    "token": str,
}

user_list_types: dict = {
    "page": int,
    "per_page": int,
    "total": int,
    "total_pages": int,
    "data": list,
    "support": dict,
}


Parameters = namedtuple("Parameters", (
    "page_digits", "strings", "large_digits",
    "user_fields", "user_required_fields",
    "incorrect_emails", "incorrect_passwords",
))

parameters: Parameters = Parameters(
    page_digits=(-1, 0, 2, 4), strings=("frr", "sks"), large_digits=(-10000, 10000),
    user_fields=("email", "name"), user_required_fields=("email", "password"),
    incorrect_emails=("qweffjo", "121425", ""), incorrect_passwords=("1", ""),
)
