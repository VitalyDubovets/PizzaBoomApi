import random


def checking_the_quality(event_data: dict) -> dict:
    event_data["goodQuality"]: bool = True
    terrible_quality: int = 9
    random_quality: int = random.randint(1, 10)
    if terrible_quality == random_quality:
        event_data["goodQuality"]: bool = False
    return event_data
