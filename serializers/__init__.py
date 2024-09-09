USER = {
    "id": None,
    "name": None,
    "email": None,
    "is_admin": None,
    "is_active": None,
    "last_login": {
        "year": None,
        "month": None,
        "day": None
    },
    "date_joined": {
        "year": None,
        "month": None,
        "day": None
    },
    "projects": {
        "id": None,
        "title": None,
        "description": None,
        "budget": None,
        "is_completed": None,
        "started": {
            "year": None,
            "month": None,
            "day": None
        }
    }
}

PROJECT = {
    "id": None,
    "title": None,
    "description": None,
    "budget": None,
    "is_completed": None,
    "started": {
        "year": None,
        "month": None,
        "day": None
    },
    "admin": {
        "id": None,
        "name": None,
        "email": None
    },
    "authors": {
        "id": None,
        "name": None,
        "email": None,
        "birth": {
            "year": None,
            "month": None,
            "day": None
        },
        "gender": None
    },
    "links": {
        "id": None,
        "value": None,
        "write": None
    }
}

LINK = {
    "id": None,
    "value": None,
    "write": None
}

AUTHOR = {
    "id": None,
    "name": None,
    "email": None,
    "birth": {
        "year": None,
        "month": None,
        "day": None
    },
    "gender": {
        "value": None
    }
}
