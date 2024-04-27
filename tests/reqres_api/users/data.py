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
    "first_name": str,
    "last_name": str,
    "avatar": str,
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
))

parameters: Parameters = Parameters(
    page_digits=(-1, 0, 2, 4), strings=("frr", "sks"), large_digits=(-10000, 10000),
)

