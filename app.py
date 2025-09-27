from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Plant  # make sure Plant model is defined in models.py
from flask_migrate import Migrate
import os

# -------------------------
# Create Flask app first
# -------------------------
app = Flask(__name__)
CORS(app)

# -------------------------
# Config
# -------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -------------------------
# Initialize db and migrate
# -------------------------
db.init_app(app)
migrate = Migrate(app, db)

# -------------------------
# GET all plants
# -------------------------
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    plants_list = [{
        "id": plant.id,
        "name": plant.name,
        "image": plant.image,
        "price": plant.price,
        "is_in_stock": plant.is_in_stock
    } for plant in plants]
    return jsonify(plants_list), 200

# -------------------------
# GET one plant by id
# -------------------------
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    return jsonify({
        "id": plant.id,
        "name": plant.name,
        "image": plant.image,
        "price": plant.price,
        "is_in_stock": plant.is_in_stock
    }), 200

# -------------------------
# PATCH one plant by id
# -------------------------
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    data = request.get_json()
    if "is_in_stock" in data:
        plant.is_in_stock = data["is_in_stock"]
    if "name" in data:
        plant.name = data["name"]
    if "price" in data:
        plant.price = data["price"]
    if "image" in data:
        plant.image = data["image"]

    db.session.commit()

    return jsonify({
        "id": plant.id,
        "name": plant.name,
        "image": plant.image,
        "price": plant.price,
        "is_in_stock": plant.is_in_stock
    }), 200

# -------------------------
# DELETE one plant by id
# -------------------------
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    db.session.delete(plant)
    db.session.commit()
    return '', 204

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
