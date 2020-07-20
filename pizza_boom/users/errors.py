from werkzeug.exceptions import HTTPException


user_errors_dict = {
    "UserNotFoundError": {
        "message": "User not found",
        "status": 404
    },
    "NotFoundRequiredDataError": {
        "message": "Required data not found. Please, fill your first name, last name and phone",
        "status": 400
    }
}


class NotFoundRequiredDataError(HTTPException):
    status: int = 400
    description: str = "Required data not found"


class UserNotFoundError(HTTPException):
    status: int = 404
    description: str = "User not found"
