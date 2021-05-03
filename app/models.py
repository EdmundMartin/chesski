from datetime import datetime
from typing import Any, Dict, List
import json

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


@login.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


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

    # TODO Add foreign key onto course - to organise puzzles

    def for_solving(self) -> Dict[str, Any]:
        response = dict()
        response["id"] = self.id
        response["name"] = self.puzzle_name
        response["startingPosition"] = self.starting_position
        response["orientation"] = self.orientation
        response["moves"] = json.loads(self.moves)
        return response


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(265))
    creator = db.Column(db.Integer, db.ForeignKey("user.id"))
    public = db.Column(db.Boolean)
    description = db.Column(db.Text)

    @staticmethod
    def courses_for_user(user_id: int) -> List['Course']:
        courses = Course.query.filter(Course.creator == user_id).all()
        return courses


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> None:
        return check_password_hash(self.password_hash, password)
