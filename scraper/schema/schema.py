import json

from jsonschema import validate


class Schema:
    def __init__(self, instance: dict, schema: dict):
        self._schema = schema
        self.instance = instance

    def validate(self):
        validate(
            instace=self.isntance, schema=self.schema
        )

        return json.dumps(self.schema)
