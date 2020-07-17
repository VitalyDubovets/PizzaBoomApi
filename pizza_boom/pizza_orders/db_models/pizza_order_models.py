import datetime
import uuid
from enum import Enum

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from pizza_boom.core.models import BaseModel


class PizzaStatus(str, Enum):
    IN_PROCESS = "in_process"
    RECEIVED = "received"


class PizzaOrder(BaseModel):
    class Meta:
        table_name: str = BaseModel.set_table_name('pizza-orders')

    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    user_id = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now())
    address = UnicodeAttribute()
    additional_phone = UnicodeAttribute(null=True)
    note = UnicodeAttribute(null=True)
    status = UnicodeAttribute(default_for_new=PizzaStatus.IN_PROCESS.value)

    execution_arn = UnicodeAttribute(null=True)
    wait_for_receive_pizza_order_token = UnicodeAttribute(null=True)
