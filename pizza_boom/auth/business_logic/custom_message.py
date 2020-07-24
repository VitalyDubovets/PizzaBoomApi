def form_email_message(event: dict) -> dict:
    event['request']['usernameParameter'] = event['userName']
    event['response']['emailSubject']: str = "Добро пожаловать в PizzaBoom"
    event['response']['emailMessage']: str = f"""
        Добро пожаловать в PizzaBoom. Ваше имя пользователя: {event['request']['usernameParameter']}.
        Временный код для подтверждения email адреса: {event['request']['codeParameter']}
    """
    return event
