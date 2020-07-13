from werkzeug.exceptions import HTTPException


user_errors_dict = {
    "UserNotFoundError": {
        "message": "User not found",
        "status": 404
    },
    "NotFoundRequestDataError": {
        "message": "Request data is empty",
        "status": 400
    }
}


class NotFoundRequestDataError(HTTPException):
    status: int = 400
    description: str = "Request data is empty"


class UserNotFoundError(HTTPException):
    status: int = 404
    description: str = "User not found"
