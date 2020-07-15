from typing import Optional, Any


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
