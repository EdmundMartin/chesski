from app import app, db, models
import unittest


class CreatePuzzleTests(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        self.resource_url: str = '/api/save-puzzle'
        db.drop_all()
        db.create_all()

    def test_create_puzzle(self):
        response = self.app.post(self.resource_url, json={
            "name": "Example Puzzle",
            "startingPosition": "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1",
            "moves": [],
            "orientation": "white"
        })
        self.assertEqual(201, response.status_code)

    def test_create_puzzle_invalid_payload(self):
        response = self.app.post(self.resource_url, json={
            "name": "Something",
            "bad_payload": "Broken",
        })
        self.assertEqual(400, response.status_code)


class LoadPuzzleTests(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
