from collections import namedtuple

correct_color_data: dict = {
    "id": 2,
    "name": "fuchsia rose",
    "year": 2001,
    "color": "#C74375",
    "pantone_value": "17-2031",
}

other_color_data: dict = {
    "id": 3,
    "name": "true red",
    "year": 2002,
    "color": "#BF1932",
    "pantone_value": "19-1664"
}


color_data_types: dict = {
    "id": int,
    "name": str,
    "year": int,
    "color": str,
    "pantone_value": str,
    "createdAt": str,
    "updatedAt": str,
}

color_list_types: dict = {
    "page": int,
    "per_page": int,
    "total": int,
    "total_pages": int,
    "data": list,
    "support": dict,
}


Parameters = namedtuple("Parameters", ("page_digits", "strings", "large_digits", "color_fields"))

parameters: Parameters = Parameters(
    page_digits=(-1, 0, 2, 4), strings=("frr", "sks"), large_digits=(-10000, 10000), color_fields=("name", "color"),
)
