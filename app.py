from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from auth import requires_auth, AuthError
from db import setup_db
from models import Movie, Actor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    # CORS Headers
    @app.after_request
    def after_request(response):

        # Allow requests headers ( Content-Type, Authorization)
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        # Allow specific requests methods (GET, POST, PATCH, DELETE, OPTIONS)
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Simple health check
    @app.route('/')
    def index():
        return "Healthy"

    # Run ONLY first time you start the app
    # db_drop_and_create_all()

    # ==================== MOVIES ==================== #

    '''
    GET /movies
    - Fetches all the movies from the database
    - Request arguments: None
    - Returns: A list of movies contain key:value pairs of id, title and
    release_date
    Response:
        {
            "success": true,
            "movies":
            [
                {
                    "id": 1,
                    "title": "Movie",
                    "release_date": "Sun, 12 July 2020 5:58:32 GMT"
                },
                {
                    "id": 2,
                    "title": "New movie",
                    "release_date": "Sun, 12 July 2020 5:58:32 GMT"
                }
            ]
        }
    '''

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):

        try:

            # Query all movies from the database
            movies = Movie.query.all()

            # Format all movies
            response = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': response
            }), 200

        except SQLAlchemyError:
            abort(422)

    '''
    POST /movies
    - Creates a movie from the request's body
    - Request arguments: None
    - Returns: the created movie contains key:value pairs of id, title and
    release_date
    Body:
        {
            "title": "The Blacklist",
            "release_date": "Sun, 12 July 2020 5:58:32 GMT"
        }
    Response:
        {
            "success": true,
            "movie":
                {
                    "id": 1,
                    "title": "The Blacklist",
                    "release_date": "Sun, 12 July 2020 5:58:32 GMT"
                }
        }
    '''

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie(payload):

        # Fetch request body
        body = request.get_json()

        # If body not provided, abort 400
        if not body:
            abort(400)

        try:

            # Retrieves the data from the body
            title = body['title']
            release_date = body['release_date']

            # if data not provided, abort 400
            if not title or not release_date:
                abort(400)

            # Check if there's matching with name
            db_movie = Movie.query.filter(Movie.title == title).one_or_none()

            # If there's matching, abort 409
            if db_movie:
                abort(409)

            # Create the new Movie and insert it in the db
            movie = Movie(title, release_date)

            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201

        except (TypeError, KeyError):
            abort(400)

        except SQLAlchemyError:
            abort(422)

    '''
    PATCH /movies/<int:id>
    - Updates a movie using the information provided by request's body
    - Request arguments: Movie id
    - Returns: the updated movie contains key:value pairs of id, title and
     release_date
    Body:
        {
            "title": "The Blacklist 8",
            "release_date": "Sun, 12 July 2020 5:58:32 GMT"
        }
    Response:
        {
            "success": true,
            "movie":
                {
                    "id": 1,
                    "title": "The Blacklist 8",
                    "release_date": "Sun, 12 July 2020 5:58:32 GMT"
                }
        }
    '''

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(movie_id, payload):

        # Fetch request body
        body = request.get_json()

        # If body not provided, abort 400
        if not body:
            abort(400)

        try:

            # Retrieves the data from the body
            title = body['title']
            release_date = body['release_date']

            # Retrieves the movie from the database
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            # If there's no such movie, abort 404
            if not movie:
                abort(404)

            # Update the model with the data provided
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date

            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

        except (TypeError, KeyError):
            abort(400)

        except SQLAlchemyError:
            abort(422)

    '''
    DELETE /movies/<int:id>
    - Updates a movie using the information provided by request's body
    - Request arguments: Movie id
    - Returns: the deleted movie id
    Response:
        {
            "success": true,
            "deleted": 1
        }
    '''

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(movie_id, payload):

        try:

            # Retrieves the movie from the database
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            # If there's no such movie, abort 404
            if not movie:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie.id
            }), 200

        except SQLAlchemyError:
            abort(422)

    # ==================== ACTORS ==================== #

    '''
    GET /actors
    - Fetches all the actors from the database
    - Request arguments: None
    - Returns: A list of actors contain key:value pairs of id, name, age and
    gender

    Response:
        {
            "success": true,
            "actors":
            [
                {
                    "id": 1,
                    "name": "John",
                    "age": 35,
                    "gender": "Male"
                },
                {
                    "id": 2,
                    "name": "Ivy",
                    "age": 34,
                    "gender": "Women"
                }
            ]
        }
    '''

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):

        try:
            # Query all actors from the database
            actors = Actor.query.all()

            # Format all actors
            response = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': response
            }), 200

        except SQLAlchemyError:
            abort(422)

    '''
    POST /actors

    - Creates an actor from the request's body
    - Request arguments: None
    - Returns: the created actor contains key:value pairs of id, name, age and
    gender

    Body:
         {
             "name": "John",
             "age": 20,
             "gender": "Women"
         }

    Response:
        {
            "success": true,
            "actor":
                {
                    "id": 1
                    "name": "John",
                    "age": 20,
                    "gender": "Women"
                }
        }
    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actor')
    def create_actor(payload):

        # Fetch request body
        body = request.get_json()

        # If body not provided, abort 400
        if not body:
            abort(400)

        try:

            # Retrieves the data from the body
            name = body['name']
            age = body['age']
            gender = body['gender']

            # if data not provided, abort 400
            if not name or not age or not gender:
                abort(400)

            # Check if there's matching with name
            db_actor = Actor.query.filter(Actor.name == name).one_or_none()

            # If there's matching, abort 409
            if db_actor:
                abort(409)

            # Create the new Actor and insert it in the db
            actor = Actor(name, age, gender)

            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201

        except (TypeError, KeyError):
            abort(400)

        except SQLAlchemyError:
            abort(422)

    '''
    PATCH /actors/<int:id>

    - Updates a actor using the information provided by request's body
    - Request arguments: Actor id
    - Returns: the updated actor contains key:value pairs of id, name, age and
    gender

    Body:
        {
            "name": "John",
            "age": 20,
            "gender": "Women"
        }

    Response:
        {
            "success": true,
            "actor":
                {
                    "id": 1,
                    "name": "John",
                    "age": 20,
                    "gender": "Women"
                }
        }
    '''

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(actor_id, payload):

        # Fetch request body
        body = request.get_json()

        # If body not provided, abort 400
        if not body:
            abort(400)

        try:

            # Retrieves the data from the body
            name = body['name']
            age = body['age']
            gender = body['gender']

            # Retrieves the movie from the database
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            # If there's no such movie, abort 404
            if not actor:
                abort(404)

            # Update the model with the data provided
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender

            actor.update()

            return jsonify({
                'success': True,
                'movie': actor.format()
            }), 200

        except (TypeError, KeyError):
            abort(400)

        except SQLAlchemyError:
            abort(422)

    '''
    DELETE /actors/<int:id>

    - Updates a movie using the information provided by request's body
    - Request arguments: Actor id
    - Returns: the deleted actor id

    Response:
        {
            "success": true,
            "deleted": 1
        }
    '''

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(actor_id, payload):

        try:

            # Retrieves the movie from the database
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            # If there's no such movie, abort 404
            if not actor:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor.id
            }), 200

        except SQLAlchemyError:
            abort(422)

    # ==================== ERROR HANDLING ==================== #

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "conflict"
        }), 409

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run()
