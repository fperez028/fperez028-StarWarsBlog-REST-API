# Star Wars Blog REST API

A RESTful API for a fictional Star Wars blog. Built with Flask and PostgreSQL, this app provides data on characters, planets, and starships. Users can also manage their own favorites.

🔗 **Live Site**: [https://flask-rest-hello-jgs1.onrender.com/](https://flask-rest-hello-jgs1.onrender.com/)
>**Note:** Render will spin down the site after 15min of no traffic, allow a moment for the site to come back up when you visit it

---

## Tech Stack

- Python 3.10
- Flask
- SQLAlchemy + Flask-Migrate
- PostgreSQL
- Pipenv
- Render.com for deployment

---

## API Overview

This API follows RESTful conventions and returns all data as JSON.

Some endpoints are public, while others require a simple `username` passed in the request body or as a query parameter.

**Base URL**: `https://flask-rest-hello-jgs1.onrender.com`

---

## Authentication

This API uses a simple username-based system:
- For GET `/user/favorites`: Pass username in `X-Username` header
- For POST favorites: Pass `username` in request body JSON
- For DELETE favorites: Pass `username` as query parameter

---

## API Endpoints

### User Endpoints

| Method | Endpoint            | Description                         | Auth Required |
|--------|---------------------|-------------------------------------|---------------|
| GET    | `/user`             | Get all users                      | No            |
| GET    | `/user/<user_id>`   | Get user by ID                     | No            |
| GET    | `/user/favorites`   | Get all favorites for a user       | Yes (Header)  |

#### Get User Favorites
```bash
curl -H "X-Username: your_username" \
  https://flask-rest-hello-jgs1.onrender.com/user/favorites
```

### Planets

| Method | Endpoint                | Description                                   | Auth Required |
|--------|-------------------------|-----------------------------------------------|---------------|
| GET    | `/planets`              | Get all planets                               | No            |
| GET    | `/planets/<planet_id>`  | Get specific planet by ID                     | No            |
| POST   | `/favorite/planet/<id>` | Add a planet to user's favorites              | Yes (Body)    |
| DELETE | `/favorite/planet/<id>` | Remove a planet from user's favorites         | Yes (Query)   |

#### Add Planet to Favorites
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username"}' \
  https://flask-rest-hello-jgs1.onrender.com/favorite/planet/1
```

#### Remove Planet from Favorites
```bash
curl -X DELETE \
  "https://flask-rest-hello-jgs1.onrender.com/favorite/planet/1?username=your_username"
```

### People

| Method | Endpoint                | Description                                  | Auth Required |
|--------|-------------------------|----------------------------------------------|---------------|
| GET    | `/people`               | Get all people                               | No            |
| GET    | `/people/<people_id>`   | Get specific person by ID                    | No            |
| POST   | `/favorite/people/<id>` | Add a person to user's favorites             | Yes (Body)    |
| DELETE | `/favorite/people/<id>` | Remove a person from user's favorites        | Yes (Query)   |

#### Add Person to Favorites
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username"}' \
  https://flask-rest-hello-jgs1.onrender.com/favorite/people/1
```

### Starships

| Method | Endpoint                   | Description                                  | Auth Required |
|--------|----------------------------|----------------------------------------------|---------------|
| GET    | `/starships`               | Get all starships                            | No            |
| GET    | `/starships/<starship_id>` | Get specific starship by ID                  | No            |
| POST   | `/favorite/starship/<id>`  | Add a starship to user's favorites           | Yes (Body)    |
| DELETE | `/favorite/starship/<id>`  | Remove a starship from user's favorites      | Yes (Query)   |

#### Add Starship to Favorites
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username"}' \
  https://flask-rest-hello-jgs1.onrender.com/favorite/starship/1
```

---

## Response Format

All endpoints return JSON responses with appropriate HTTP status codes:

### Success Responses
- `200`: Successful GET request
- `201`: Successful resource creation
- `404`: Resource not found
- `400`: Bad request (missing data, duplicate favorites, etc.)

### Sample Response - Get All Planets
```json
[
  {
    "id": 1,
    "name": "Tatooine",
    "diameter": "10465",
    "climate": "arid",
    "terrain": "desert",
    "population": "200000"
  },
  {
    "id": 2,
    "name": "Alderaan",
    "diameter": "12500",
    "climate": "temperate",
    "terrain": "grasslands, mountains",
    "population": "2000000000"
  }
]
```

### Sample Response - User Favorites
```json
[
  {
    "id": 1,
    "user_id": 1,
    "planet_id": 1,
    "person_id": null,
    "starship_id": null
  },
  {
    "id": 2,
    "user_id": 1,
    "planet_id": null,
    "person_id": 1,
    "starship_id": null
  }
]
```

---

## Error Handling

The API returns consistent error messages:

```json
{
  "error": "User not found"
}
```

```json
{
  "error": "Favorite already exists"
}
```

---

## Database Models

The API uses four main models:

- **User**: Contains user information and relationships to favorites
- **Person**: Star Wars characters (Luke Skywalker, Darth Vader, etc.)
- **Planet**: Star Wars planets (Tatooine, Alderaan, etc.)
- **Starship**: Star Wars vehicles (Millennium Falcon, Death Star, etc.)
- **Favorite**: Junction table linking users to their favorite items
