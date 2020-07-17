import json
from typing import Any, Optional


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


def merge(source: dict, destination: dict) -> dict:
    """
    Deep merges source into destination

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(b, a) == { 'first' : { 'all_rows' : {
        'pass' : 'dog', 'fail' : 'cat', 'number' : '5'
    } } }
    True
    """
    if source:
        for key, value in list(source.items()):
            node: Optional[dict] = destination.setdefault(key, {})

            if isinstance(value, dict) and isinstance(node, dict):
                merge(value, node)
            else:
                destination[key]: Any = value

    return destination
