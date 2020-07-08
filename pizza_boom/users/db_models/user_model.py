import uuid

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from core.models.base_model import BaseModel


class UserModel(BaseModel):
    class Meta:
        table_name: str = BaseModel.set_table_name('users')

    id = UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    email = UnicodeAttribute()
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    last_sign_in = UTCDateTimeAttribute()
