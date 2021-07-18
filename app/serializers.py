from marshmallow import Schema, fields


class Move(Schema):
    # TODO - We need to record promotions!
    start = fields.Str()
    end = fields.Str()


class PuzzleSchema(Schema):
    name = fields.Str()
    starting_position = fields.Str(data_key="startingPosition")
    moves = fields.List(fields.Nested(Move))
    orientation = fields.Str()
    before_text = fields.Str(required=False)
    after_text = fields.Str(required=False)
