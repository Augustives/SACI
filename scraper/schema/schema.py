from jsonschema import validate


class Schema:
    def __init__(self, instance: dict, schema: dict):
        self._schema = schema
        self.instance = instance

    def validate(self):
        validate(
            instance=self.instance, schema=self._schema
        )

        return self.instance
