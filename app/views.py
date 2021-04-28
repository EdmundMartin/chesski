import json
from datetime import datetime

from flask import send_from_directory, request, jsonify

from app import app, db
from app.models import ChessPuzzle
from app.sm_algorithm import SuperMemoAlgorithm


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
def puzzles():
    return send_from_directory("templates", "board.html")


@app.route("/add-puzzle")
def add_puzzle():
    return send_from_directory("templates", "add-puzzle.html")


@app.route("/api/save-puzzle", methods=["POST"])
def save_puzzle():
    # TODO - Set mime type to application/json to leverage Flask built ins
    payload = json.loads(request.data)
    name = payload["name"]
    starting_position = payload["startingPosition"]
    moves = json.dumps(payload["moves"])
    orientation = payload["orientation"]
    puzzle = ChessPuzzle(
        puzzle_name=name,
        starting_position=starting_position,
        moves=moves,
        orientation=orientation,
    )
    db.session.add(puzzle)
    db.session.commit()
    return ""


@app.route("/api/load-puzzle", methods=["GET"])
def load_puzzle():
    puzzle: ChessPuzzle = ChessPuzzle.query.order_by(
        ChessPuzzle.next_review_due
    ).first()
    return jsonify(puzzle.for_solving())


@app.route("/api/passed-puzzle/<int:puzzle_id>", methods=["POST"])
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
    return ""


@app.route("/api/failed-puzzle/<int:puzzle_id>", methods=["POST"])
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
    return ""
