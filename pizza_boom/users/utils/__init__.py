import structlog


logger = structlog.get_logger()


def get_cognito_user_data(event: dict) -> dict:
    """
    Get information about authorized user from AWS event
    :param event: Information of event
    :return: User's data
    """
    try:
        user_data: dict = event['requestContext']['authorizer'].get('claims')
    except KeyError:
        logger.debug(
            "catch_error_of_user_data",
            error_data=event
        )
        raise Exception("Invalid user's data")
    return user_data
