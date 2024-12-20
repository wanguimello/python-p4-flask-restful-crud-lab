#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(
    __name__, static_url_path="/static", static_folder="../client/public/images"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        # Get all plants and return them as a list of dictionaries
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        # Add a new plant
        data = request.get_json()

        # Validate input data
        if not all(key in data for key in ["name", "image", "price"]):
            return make_response({"error": "Missing required fields"}, 400)

        new_plant = Plant(
            name=data["name"],
            image=data["image"],
            price=data["price"],
            is_in_stock=data.get("is_in_stock", True),  # Default to True if not provided
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, "/plants")


class PlantByID(Resource):
    def get(self, id):
        # Fetch plant by ID
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        return make_response({"error": "Plant not found"}, 404)

    def patch(self, id):
        # Update an existing plant
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        data = request.get_json()
        
        # Update fields only if they are provided in the request
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]
        if "price" in data:
            plant.price = data["price"]

        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        # Delete a plant
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        db.session.delete(plant)
        db.session.commit()
        return make_response("", 204)


api.add_resource(PlantByID, "/plants/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
