from app import db


class ChessPuzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_name = db.Column(db.String(265))
    starting_position = db.Column(db.String(265))
    orientation = db.Column(db.String(12))
    # TODO Move to postgres to make use of JSON format
    moves = db.Column(db.Text)
