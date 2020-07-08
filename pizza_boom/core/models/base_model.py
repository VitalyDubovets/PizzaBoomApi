import os

from pynamodb.models import Model


class BaseModel(Model):
    class Meta:
        table_name: str = NotImplemented

    @staticmethod
    def set_table_name(name: str) -> str:
        return f"pizza-boom-{os.getenv('STAGE')}-{name}"
