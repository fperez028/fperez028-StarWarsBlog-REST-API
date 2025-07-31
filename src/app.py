"""
This module starts the API Server, loads the DB, and adds endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Starship, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

# Database setup
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Test route
@app.route('/user', methods=['GET'])
def handle_hello():
    return jsonify({"msg": "Hello, this is your GET /user response"}), 200

# USERS
@app.route("/api/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route("/api/users/favorites", methods=["GET"])
def get_user_favorites():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required as query param"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorites = [fav.serialize() for fav in user.favorites]
    return jsonify(favorites), 200

# FAVORITES
@app.route("/api/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    username = request.json.get("username")
    user = User.query.filter_by(username=username).first()
    planet = Planet.query.get(planet_id)

    if not user or not planet:
        return jsonify({"error": "User or planet not found"}), 404

    existing = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    if existing:
        return jsonify({"error": "Favorite already exists"}), 400

    favorite = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route("/api/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    username = request.args.get("username")
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet removed"}), 200

@app.route("/api/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_person(people_id):
    username = request.json.get("username")
    user = User.query.filter_by(username=username).first()
    person = Person.query.get(people_id)

    if not user or not person:
        return jsonify({"error": "User or person not found"}), 404

    existing = Favorite.query.filter_by(user_id=user.id, person_id=people_id).first()
    if existing:
        return jsonify({"error": "Favorite already exists"}), 400

    favorite = Favorite(user_id=user.id, person_id=person.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route("/api/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_person(people_id):
    username = request.args.get("username")
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorite = Favorite.query.filter_by(user_id=user.id, person_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite person removed"}), 200

@app.route("/api/favorite/starship/<int:starship_id>", methods=["POST"])
def add_favorite_starship(starship_id):
    username = request.json.get("username")
    user = User.query.filter_by(username=username).first()
    starship = Starship.query.get(starship_id)

    if not user or not starship:
        return jsonify({"error": "User or starship not found"}), 404

    existing = Favorite.query.filter_by(user_id=user.id, starship_id=starship_id).first()
    if existing:
        return jsonify({"error": "Favorite already exists"}), 400

    favorite = Favorite(user_id=user.id, starship_id=starship.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route("/api/favorite/starship/<int:starship_id>", methods=["DELETE"])
def delete_favorite_starship(starship_id):
    username = request.args.get("username")
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorite = Favorite.query.filter_by(user_id=user.id, starship_id=starship_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite starship removed"}), 200

# PEOPLE
@app.route("/api/people", methods=["GET"])
def get_all_people():
    people = Person.query.all()
    return jsonify([p.serialize() for p in people]), 200

@app.route("/api/people/<int:people_id>", methods=["GET"])
def get_single_person(people_id):
    person = Person.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

# PLANETS
@app.route("/api/planets", methods=["GET"])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route("/api/planets/<int:planet_id>", methods=["GET"])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# STARSHIPS
@app.route("/api/starships", methods=["GET"])
def get_all_starships():
    starships = Starship.query.all()
    return jsonify([s.serialize() for s in starships]), 200

@app.route("/api/starships/<int:starship_id>", methods=["GET"])
def get_single_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if not starship:
        return jsonify({"error": "Starship not found"}), 404
    return jsonify(starship.serialize()), 200

# Main entry point
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
