from marshmallow import Schema, fields
from marshmallow import ValidationError as mmValidationError

class CouriersPostValidator:

    def __init__(self):
        class Courier(Schema):
            courier_id = fields.Int()
            courier_type = fields.Str()
            regions = fields.List(fields.Int())
            working_hours = fields.List(fields.Str())

        class Post(Schema):
            data = fields.List(fields.Nested(Courier))

        self.schema = Post()

    @staticmethod
    def validate(self):
        try:
            return schema.load(self.data)
        except mmValidationError as err:
            print(err)
        return self.schema.validate()

