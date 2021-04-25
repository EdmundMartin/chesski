from flask import render_template, send_from_directory
from app import app


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
