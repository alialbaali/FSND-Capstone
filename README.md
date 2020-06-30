# Casting Agency

#### Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

#### [Link](https://casting-agency-udacity-capston.herokuapp.com/).

## Motivation

This is my Capstone (Casting Agency) project for the Udacity FSND.

## Dependencies

Dependencies are listed in the `requirements.txt` file. 
Run `pip3 install -r requirements.txt` to install them.

## Roles

There are three Roles in this API

##### Casting Assistant
##### Casting Director
##### Executive Producer

All tokens are in the `setup.sh` file

## Endpoints

## Movies

### `GET /movies`

##### `Public`

- Fetches all the movies from the database
- Request arguments: None
- Returns: A list of movies contain key:value pairs of id, title and release_date

#### `Response`

```json5
{
  "success": true,
  "movies": [
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
```

### `POST /movies`

##### `Executive Producer`

- Creates a movie from the request's body
- Request arguments: None
- Returns: the created movie contains key:value pairs of id, title and release_date

#### `Body`

```json5
{
  "title": "The Blacklist",
  "release_date": "Sun, 12 July 2020 5:58:32 GMT"
}
```

#### `Response`

```json5
{
  "success": true,
  "movie": {
     "id": 1,
    "title": "The Blacklist",
    "release_date": "Sun, 12 July 2020 5:58:32 GMT"
  }
}
```

### `PATCH /movies/<int:id>`

##### `Casting Director or Executive Producer`

- Updates a movie using the information provided by request's body
- Request arguments: Movie id
- Returns: the updated movie contains key:value pairs of id, title and release_date

#### `Body`

```json5
{
  "title": "The Blacklist 8",
  "release_date": "Sun, 12 July 2020 5:58:32 GMT"
}
```

#### `Response`

```json5
{
  "success": true,
  "movie": {
     "id": 1,
    "title": "The Blacklist 8",
    "release_date": "Sun, 12 July 2020 5:58:32 GMT"
  }
}
```

### `DELETE /movies/<int:id>`

##### `Executive Producer`

- Deletes a movie based the request argument
- Request arguments: Movie id
- Returns: the deleted movie id

#### `Response`

```json5
{
  "success": true,
  "deleted": 1 
}
```

## Actors

### `GET /actors`

##### `Public`

- Fetches all the actors from the database
- Request arguments: None
- Returns: A list of actors contain key:value pairs of id, name, age and gender

#### `Response`

```json5
{
  "success": true,
  "actors": [
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
```

### `POST /actors`

##### `Casting Director or Executive Producer`

- Creates an actor from the request's body
- Request arguments: None
- Returns: the created actor contains key:value pairs of id, name, age and gender

#### `Body`

```json5
{
  "name": "John",
  "age": 20,
  "gender": "Women"
}
```

#### `Response`

```json5
{
  "success": true,
  "actor": {
     "id": 1,
     "name": "John",
     "age": 20,
     "gender": "Women"
  }
}
```

### `PATCH /actors/<int:id>`

##### `Casting Director or Executive Producer`

- Updates a actor using the information provided by request's body
- Request arguments: Actor id
- Returns: the updated actor contains key:value pairs of id, name, age and gender

#### `Body`

```json5
{
  "name": "John",
  "age": 20,
  "gender": "Women"
}
```

#### `Response`

```json5
{
  "success": true,
  "actor": {
     "id": 1,
     "name": "John",
     "age": 20,
     "gender": "Women"
  }
}
```

### `DELETE /actors/<int:id>`

##### `Casting Director or Executive Producer`

- Deletes an actor based the request argument
- Request arguments: Actor id
- Returns: the deleted actor id

#### `Response`

```json5
{
  "success": true,
  "deleted": 1 
}
```

## Status Codes

- `200` : Request has been fulfilled
- `201` : Entity has been created
- `400` : Missing parameters or body
- `401` : Unauthorized 
- `403` : Lack of specific permission
- `404` : Resource not found
- `409` : Conflict when creating a new entity
- `422` : Wrong info provided

## Tests

To run the tests, run `python3 tests.py`.
