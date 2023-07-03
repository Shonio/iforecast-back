from werkzeug.exceptions import HTTPException


class CustomBadRequest(HTTPException):
    code = 400
    description = "Bad Request"
