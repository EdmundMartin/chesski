import json
from flask import render_template, send_from_directory, request, jsonify
from app import app, db
from app.models import ChessPuzzle


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/img/chesspieces/wikipedia/<path:path>')
def send_pieces(path):
    return send_from_directory('img', path)


@app.route('/')
def puzzles():
    return send_from_directory('templates', 'board.html')


@app.route('/add-puzzle')
def add_puzzle():
    return send_from_directory('templates', 'add-puzzle.html')


@app.route('/api/save-puzzle', methods=['POST'])
def save_puzzle():
    payload = json.loads(request.data)
    print(payload)
    name = payload['name']
    starting_position = payload['startingPosition']
    moves = json.dumps(payload['moves'])
    orientation = payload['orientation']
    """
    puzzle_name = db.Column(db.String(265))
    starting_position = db.Column(db.String(265))
    orientation = db.Column(db.String(12))
    moves = db.Column(db.Text)
    
    puzzle = ChessPuzzle(puzzle_name=name, starting_position=starting_position, moves=moves,
                         orientation=)
    """
    puzzle = ChessPuzzle(puzzle_name=name, starting_position=starting_position, moves=moves,
                         orientation=orientation)
    db.session.add(puzzle)
    db.session.commit()
    return ''


@app.route('/api/load-puzzle', methods=['GET'])
def load_puzzle():
    puzzle: ChessPuzzle = ChessPuzzle.query.first()
    response = {}
    response['name'] = puzzle.puzzle_name
    response['startingPosition'] = puzzle.starting_position
    response['orientation'] = puzzle.orientation
    response['moves'] = json.loads(puzzle.moves)
    print(response['moves'])
    return jsonify(response)