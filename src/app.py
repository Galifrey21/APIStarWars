"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

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


people_list = [
    {"id":1,"name":"Cassian","locations":"Kenari","gender":"Male","dimensions":"Height: 1.78m","weapons":"BlasTech A280-CFE"},
    {"id":2,"name":"Mon Mothma","locations":"Coruscant","gender":"Female","dimensions":"Height: 1.5m","weapons":"BlasTech A280-CFE"},
    {"id":3,"name":"Luthen Rael","locations":"Coruscant","gender":"Male","dimensions":"Height: 1.78m","weapons":"BlasTech A280-CFE"}
]
planet_list=[
    {"id":1,"name":"Aeos Prime","Appearances":"Star Wars Resistance"},
    {"id":2,"name":"Agamar","Appearances":"Star Wars Rebels"},
    {"id":3,"name":"Ahch-To","Appearances":"Star Wars: The Last Jedi (Episode VIII)"}
]

users_list = [
    {"id": 1, "name": "Alice", "email": "alice@gmail.com","favorites_people":[],"favorites_planets":[]},
    {"id": 2, "name": "Bob", "email": "bob@gmail.com","favorites_people":[],"favorites_planets":[]},
    {"id": 3, "name": "Oscar", "email": "racso@gmail.com","favorites_people":[],"favorites_planets":[]}

]

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    return jsonify(people_list)

@app.route('/people/<int:id>', methods=['GET'])
def get_person_by_id(id):
    person = next((person for person in people_list if person['id'] == id), None)
    
    if person is None:
        return jsonify({"error": "Person not found"}), 404

    return jsonify(person), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    return jsonify(planet_list)

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = next((planet for planet in planet_list if planet['id'] == id), None)
    
    if planet is None:
        return jsonify({"error": "Person not found"}), 404

    return jsonify(planet), 200

@app.route('/users',methods=['GET'])
def get_users():
    return jsonify(users_list)

@app.route('/users/favorites', methods=['GET'])
def get_all_users_favorites():

    all_favorites = []

    for user in users_list:
        favorite_people = [person['name'] for person in people_list if person['id'] in user['favorites_people']]
        favorite_planets = [planet['name'] for planet in planet_list if planet['id'] in user['favorites_planets']]
        
        favorites_data = {
            "user_id": user['id'],
            "name": user['name'],
            "favorites_people": favorite_people,
            "favorites_planets": favorite_planets
        }
        all_favorites.append(favorites_data)
    
    return jsonify(all_favorites), 200

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_people_to_favorites(user_id, people_id):
    
    user = next((user for user in users_list if user['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    people = next((people for people in people_list if people['id'] == people_id), None)
    
    if people is None:
        return jsonify({"error": "People not found"}), 404
    
    if people_id not in user["favorites_people"]:
        user["favorites_people"].append(people_id)
    
    return jsonify({"message": "People added to favorites", "favorites_people": user["favorites_people"]}), 200

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_planet_to_favorites(user_id, planet_id):
   
    user = next((user for user in users_list if user['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    planet = next((planet for planet in planet_list if planet['id'] == planet_id), None)
    
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    if planet_id not in user["favorites_planets"]:
        user["favorites_planets"].append(planet_id)
    
    return jsonify({"message": "Planet added to favorites", "favorites_planets": user["favorites_planets"]}), 200

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_people_from_favorites(user_id, people_id):
    user = next((user for user in users_list if user['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    if people_id not in user["favorites_people"]:
        return jsonify({"error": "People not found in favorites"}), 404
    
    user["favorites_people"].remove(people_id)
    
    return jsonify({"message": "People removed from favorites", "favorites_people": user["favorites_people"]}), 200

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_planet_from_favorites(user_id, planet_id):

    user = next((user for user in users_list if user['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    if planet_id not in user["favorites_planets"]:
        return jsonify({"error": "Planet not found in favorites"}), 404
    
    user["favorites_planets"].remove(planet_id)
    
    return jsonify({"message": "Planet removed from favorites", "favorites_planets": user["favorites_planets"]}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
