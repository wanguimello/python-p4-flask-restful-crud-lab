#!/usr/bin/env python3

from app import app
from models import db, Plant


# Function to seed initial data
def seed_plants():
    with app.app_context():
        # Clear existing data
        print("Deleting existing data...")
        db.session.query(Plant).delete()

        # Add initial plant data
        plants = [
            Plant(
                id=1,
                name="Aloe",
                image="http://localhost:4000/images/aloe.jpg",
                price=11.50,
                is_in_stock=True,
            ),
            Plant(
                id=2,
                name="ZZ Plant",
                image="http://localhost:4000/images/zz-plant.jpg",
                price=25.98,
                is_in_stock=False,
            ),
            Plant(
                id=3,
                name="Snake Plant",
                image="http://localhost:4000/images/snake-plant.jpg",
                price=19.99,
                is_in_stock=True,
            ),
        ]

        # Insert new data into the database
        print("Adding new data...")
        db.session.add_all(plants)
        db.session.commit()
        print("Database seeded successfully!")


# Run the seed function
if __name__ == "__main__":
    seed_plants()