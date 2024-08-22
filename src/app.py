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
from models import db, User, People, Planets, Favorite
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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

################################################################################################################################################################
# Users Enpoints
@app.route('/users', methods=['GET'])
def get_all_users():   
    users = User.query.all()

    return jsonify([user.serialize() for user in users]), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Verifica si el usuario ya existe
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'User already exists'}), 400

    # Crea un nuevo usuario
    user = User(id=User.query.count() + 1, email=email, password=password, is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


################################################################################################################################################################
# People Enpoints

@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    all_people = [person.serialize() for person in people]

    return jsonify(all_people), 200

@app.route("/people/<int:people_id>", methods=["GET"])
def get_person(people_id):
    people = People.query.get(people_id)

    if people is None:
        return jsonify({"error": "No people with this id"}), 404
    return jsonify(people.serialize()), 200

# No aplicaría los métodos POST Y DELETE en People
@app.route('/people', methods=['POST'])
def create_person():
    data = request.get_json()
    
    person = People(id=People.query.count() + 1, **data)
    db.session.add(person)
    db.session.commit()


    return jsonify(person.serialize()), 201

@app.route("/people/<int:people_id>", methods=["DELETE"])
def delete_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "person not found"}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Person deleted"}), 200


################################################################################################################################################################
# Planets Enpoints

@app.route("/planets", methods=["GET"])
def get_all_planets():
    planets = Planets.query.all()

    return jsonify([planet.serialize() for planet in planets])

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize())

# No aplicaría los métodos POST Y DELETE en People

@app.route("/planets", methods=["POST"])
def create_planet():
    data = request.get_json()

    planet = Planets(id=Planets.query.count()+ 1, **data)
    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.serialize()), 201


@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"error": "planet not found"}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": "Planet deleted"}), 200


################################################################################################################################################################
# Favorite Enpoints

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.first()  
    favorites = Favorite.query.filter_by(user_id=user.id).all()  
    return jsonify([favorite.serialize() for favorite in favorites])


@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.first() 
    new_favorite = Favorite(user_id=user.id, planet_id=planet_id) 
    db.session.add(new_favorite)  
    db.session.commit() 
    return jsonify({'message': 'Favorite planet added successfully'}), 201  


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user = User.query.first()  
    new_favorite = Favorite(user_id=user.id, people_id=people_id)  
    db.session.add(new_favorite)  
    db.session.commit()  
    return jsonify({'message': 'Favorite person added successfully'}), 201


@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user = User.query.first()  
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()  
    if favorite:
        db.session.delete(favorite)  
        db.session.commit()  
        return jsonify({'message': 'Favorite planet removed successfully'})  
    return jsonify({'message': 'Favorite not found'}), 404 


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user = User.query.first() 
    favorite = Favorite.query.filter_by(user_id=user.id, people_id=people_id).first()  
    if favorite:
        db.session.delete(favorite)  
        db.session.commit()  
        return jsonify({'message': 'Favorite person removed successfully'}) 
    return jsonify({'message': 'Favorite not found'}), 404 





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
