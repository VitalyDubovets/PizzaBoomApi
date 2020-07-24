import json
from typing import Optional


def make_response(message_body: Optional[dict], status_code: int) -> dict:
    """
    Generate response body for AWS http
    :param message_body: Your response body
    :param status_code: HTTP status code
    :return: Generated response
    """
    return {
        'statusCode': status_code,
        'body': json.dumps(message_body)
    }
