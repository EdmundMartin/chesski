from app import db
from datetime import datetime
from typing import Any, Dict
import json


class ChessPuzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_name = db.Column(db.String(265))
    starting_position = db.Column(db.String(265))
    orientation = db.Column(db.String(12))
    # TODO Move to postgres to make use of JSON format
    ease = db.Column(db.Float, nullable=True)
    repetitions = db.Column(db.Integer, nullable=True)
    interval = db.Column(db.Float, nullable=True)
    next_review_due = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    moves = db.Column(db.Text)

    def for_solving(self) -> Dict[str, Any]:
        response = dict()
        response['id'] = self.id
        response['name'] = self.puzzle_name
        response['startingPosition'] = self.starting_position
        response['orientation'] = self.orientation
        response['moves'] = json.loads(self.moves)
        return response
