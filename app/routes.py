from datetime import datetime
import json
from typing import Any, Dict

from flask import (
    send_from_directory,
    request,
    jsonify,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_required, current_user
from marshmallow.exceptions import ValidationError

from app import app, db
from app.models import ChessPuzzle, Course
from app.sm_algorithm import SuperMemoAlgorithm
from app.serializers import PuzzleSchema
from app.forms import CourseForm


@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("css", path)


@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("js", path)


@app.route("/img/chesspieces/wikipedia/<path:path>")
def send_pieces(path):
    return send_from_directory("img", path)


@app.route("/")
@login_required
def puzzles():
    return send_from_directory("templates", "board.html")


@app.route("/add-puzzle")
@login_required
def add_puzzle():
    return send_from_directory("templates", "add-puzzle.html")


@app.route("/create-course", methods=["GET", "POST"])
@login_required
def create_course():
    user_id: int = current_user.id
    form = CourseForm()
    if form.validate_on_submit():
        created_course = Course(
            name=form.name.data,
            creator=user_id,
            public=form.public.data,
            description=form.description.data,
        )
        db.session.add(created_course)
        db.session.commit()
        return redirect(url_for("puzzles"))
    return render_template("create-course.html", form=form)


@app.route("/my-courses", methods=["GET", "POST"])
@login_required
def course_list():
    all_courses = Course.courses_for_user(current_user.id)
    return render_template("list-courses.html", courses=all_courses)


@app.route("/api/save-puzzle", methods=["POST"])
@login_required
def save_puzzle():
    try:
        result: Dict[str, Any] = PuzzleSchema().load(request.json)
    except ValidationError:
        return jsonify({"status": "failure", "message": "Invalid payload"}), 400
    puzzle = ChessPuzzle(
        puzzle_name=result["name"],
        starting_position=result["starting_position"],
        moves=json.dumps(result["moves"]),
        orientation=result["orientation"],
    )
    db.session.add(puzzle)
    db.session.commit()
    return jsonify({"status": "success"}), 201


@app.route("/api/load-puzzle", methods=["GET"])
@login_required
def load_puzzle():
    puzzle: ChessPuzzle = ChessPuzzle.query.order_by(
        ChessPuzzle.next_review_due
    ).first()
    if puzzle is None:
        return jsonify({"error": "No puzzles in database"}), 400
    return jsonify(puzzle.for_solving())


@app.route("/api/passed-puzzle/<int:puzzle_id>", methods=["POST"])
@login_required
def puzzle_passed(puzzle_id: int):
    puzzle: ChessPuzzle = ChessPuzzle.query.get(puzzle_id)
    if puzzle.repetitions is None:
        super_memo: SuperMemoAlgorithm = SuperMemoAlgorithm.first_review(5)
    else:
        super_memo: SuperMemoAlgorithm = SuperMemoAlgorithm(
            puzzle.ease, puzzle.interval, puzzle.repetitions
        )
        super_memo.review(5, datetime.now())
    puzzle.repetitions = super_memo.repetitions
    puzzle.ease = super_memo.ease
    puzzle.interval = super_memo.interval
    puzzle.next_review_due = super_memo.review_date
    db.session.commit()
    return jsonify({"status": "success"})


@app.route("/api/failed-puzzle/<int:puzzle_id>", methods=["POST"])
@login_required
def puzzle_failed(puzzle_id: int):
    puzzle: ChessPuzzle = ChessPuzzle.query.get(puzzle_id)
    if puzzle.repetitions is None:
        super_memo: SuperMemoAlgorithm = SuperMemoAlgorithm.first_review(0)
    else:
        super_memo: SuperMemoAlgorithm = SuperMemoAlgorithm(
            puzzle.ease, puzzle.interval, puzzle.repetitions
        )
        super_memo.review(0, datetime.now())
    puzzle.repetitions = super_memo.repetitions
    puzzle.ease = super_memo.ease
    puzzle.interval = super_memo.interval
    puzzle.next_review_due = super_memo.review_date
    db.session.commit()
    return jsonify({"status": "success"}), 201
