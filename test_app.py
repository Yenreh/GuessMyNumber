import unittest
from app import app
from flask import session
from unittest.mock import patch

class TestGuessMyNumberGame(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'your_secret_key'
        self.client = app.test_client()

    # la página carga
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Set a maximum number to start the game', response.data)

    # más alto o más bajo
    def test_guess_higher(self):
        self.client.post('/set_max', data={'max_number': 10}, follow_redirects=True) 
        response = self.client.post('/guess', data={'guess': 5}, follow_redirects=True)
        self.assertIn(b'Higher!', response.data)

    def test_guess_lower(self):
        self.client.post('/set_max', data={'max_number': 10}, follow_redirects=True) 
        response = self.client.post('/guess', data={'guess': 15}, follow_redirects=True)
        self.assertIn(b'Lower!', response.data)

    # acierto
    @patch('random.randint', return_value=5)  # Simulo el número aleatorio como 5
    def test_guess_correct(self, mock_randint):
        self.client.post('/set_max', data={'max_number': 10}, follow_redirects=True)
        response = self.client.post('/guess', data={'guess': '5'}, follow_redirects=True)
        self.assertIn(b'Correct!', response.data)

    # reiniciar
    def test_new_game(self):
        self.client.post('/set_max', data={'max_number': 10}, follow_redirects=True)
        self.client.post('/guess', data={'guess': 5}, follow_redirects=True)
        response = self.client.get('/new_game', follow_redirects=True)
        self.assertIn(b'Set a maximum number to start the game', response.data)

    # entrada no válida
    def test_invalid_guess(self):
        self.client.post('/set_max', data={'max_number': 10}, follow_redirects=True)
        response = self.client.post('/guess', data={'guess': 'invalid'}, follow_redirects=True)
        self.assertIn(b'Please enter a valid number!', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
