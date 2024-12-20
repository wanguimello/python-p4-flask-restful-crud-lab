from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Plant(db.Model, SerializerMixin):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Plant {self.name} | In Stock: {self.is_in_stock}>"

    @classmethod
    def update_plant(cls, plant_id, is_in_stock):
        """
        Updates the `is_in_stock` attribute for a specific plant.
        """
        plant = cls.query.get(plant_id)
        if not plant:
            return None
        plant.is_in_stock = is_in_stock
        db.session.commit()
        return plant

    @classmethod
    def delete_plant(cls, plant_id):
        """
        Deletes a specific plant by its ID.
        """
        plant = cls.query.get(plant_id)
        if not plant:
            return None
        db.session.delete(plant)
        db.session.commit()
        return True