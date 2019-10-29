from datetime import datetime
import json
from dataclasses import is_dataclass
from moneyed import Money


class PartData(dict):

    def __init__(self):
        super().__init__()
        self.timestamp: datetime = datetime.now()

    def to_json(self) -> str:
        class CustomEncoder(json.JSONEncoder):
            def default(self, o):
                if is_dataclass(o):
                    return o.__dict__
                if isinstance(o, Money):
                    return o.currency.code, str(o.amount)
                if isinstance(o, datetime):
                    return str(o)
                raise TypeError("Not JSON serializable!")
        return json.dumps(self, indent=4, cls=CustomEncoder)
