import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import APP
from db import setup_db

DATABASE_NAME = "capstone_test"
DATABASE_PATH = f"postgresql://postgres:135792468@localhost:5432/{DATABASE_NAME}"

ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')

ASSISTANT_AUTH_HEADER = {'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
DIRECTOR_AUTH_HEADER = {'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
PRODUCER_AUTH_HEADER = {'Authorization': f'Bearer {PRODUCER_TOKEN}'}


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        self.database_path = DATABASE_PATH
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.movie = {
            'title': 'The Blacklist',
            'release_date': 'Sun, 24 May 2020 13:04:03 GMT'
        }

        self.actor = {
            'name': 'John Wick',
            'age': 44,
            'gender': 'Male'
        }

    def test_get_movies(self):
        res = self.client().get('/movies', headers=ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_401_get_movies_unauthorized(self):
        res = self.client().get('/movies', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertFalse(len(data['movies']))

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.movie, headers=DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_401_create_movie_unauthorized(self):
        res = self.client().post('/movies', json=self.movie, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_400_create_movie_with_no_body(self):
        res = self.client().post('/movies', json='', headers=DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json=self.movie, headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_400_update_movie_with_no_body(self):
        res = self.client().patch('/movies/1000', json='', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_401_update_movie_unauthorized(self):
        res = self.client().patch('movies/1', json=self.movie, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/1000', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_delete_movie_unauthorized(self):
        res = self.client().delete('/movies/1', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # actors endpoint tests

    def test_get_actors(self):
        res = self.client().get('/actors', headers=ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_401_get_actors_unauthorized(self):
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertFalse(len(data['movies']))

    def test_create_actor(self):
        res = self.client().post('/actors', json=self.actor, headers=DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_401_create_actor_unauthorized(self):
        res = self.client().post('/actors', json=self.actor, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_400_create_actor_with_no_body(self):
        res = self.client().post('/actors', json='', headers=DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_update_actor(self):
        res = self.client().patch('/actors/1', json=self.actor, headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_400_update_actor_with_no_body(self):
        res = self.client().patch('/actors/1000', json='', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_401_update_actor_unauthorized(self):
        res = self.client().patch('actors/1', json=self.actor, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/1000', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_401_delete_actors_unauthorized(self):
        res = self.client().delete('/actors/1', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


if __name__ == '__main__':
    unittest.main()
