from enum import Enum


class CodeStatus(Enum):
    CREATE = 201
    GET = 200
    PATCH = 200
    DELETE = 204
    SERVER_ERR = 500
    CLIENT_ERR = 404
