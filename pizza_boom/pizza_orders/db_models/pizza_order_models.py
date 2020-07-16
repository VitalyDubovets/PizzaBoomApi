import uuid
from enum import Enum

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from pizza_boom.core.models import BaseModel


class PizzaStatus(str, Enum):
    IN_PROCESS = "in_process"
    RECEIVED = "received"


class PizzaOrder(BaseModel):
    id = UnicodeAttribute(default=lambda: str(uuid.uuid4()))
    created_at = UTCDateTimeAttribute()
    status = UnicodeAttribute(default_for_new=PizzaStatus.IN_PROCESS.value)
    wait_for_receive_pizza_order_token = UnicodeAttribute(null=True)
