import json
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat() + "Z"

        return json.JSONEncoder.default(self, o)