from jsonschema import validate
from scraper.schema.scraper_output_schema import scraper_output


class Schema:
    def __init__(self, instance: dict, schema: dict):
        self._schema = schema
        self.instance = instance

    def validate(self):
        validate(instance=self.instance, schema=self._schema)


SCRAPER_OUTPUT = scraper_output
