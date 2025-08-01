from src.models import db, Person, Planet, Starship
from src.app import app

def seed_data():
    with app.app_context():
        # Clear existing data (optional but useful for dev)
        db.session.query(Person).delete()
        db.session.query(Planet).delete()
        db.session.query(Starship).delete()

        # Add people
        people = [
            Person(
                name="Luke Skywalker",
                birth_year="19BBY",
                eye_color="blue",
                gender="male",
                hair_color="blond",
                height=172.0,
                mass=77.0,
                skin_color="fair",
                homeworld="https://www.swapi.tech/api/planets/1"
            ),
            Person(
                name="Leia Organa",
                birth_year="19BBY",
                eye_color="brown",
                gender="female",
                hair_color="brown",
                height=150.0,
                mass=49.0,
                skin_color="light",
                homeworld="https://www.swapi.tech/api/planets/2"
            ),
            Person(
                name="Darth Vader",
                birth_year="41.9BBY",
                eye_color="yellow",
                gender="male",
                hair_color="none",
                height=202.0,
                mass=136.0,
                skin_color="white",
                homeworld="https://www.swapi.tech/api/planets/1"
            ),
        ]

        # Add planets
        planets = [
            Planet(
                name="Tatooine",
                climate="arid",
                diameter=10465.0,
                gravity="1 standard",
                orbital_period=304.0,
                population=200000.0,
                rotation_period=23.0,
                surface_water=1.0,
                terrain="desert"
            ),
            Planet(
                name="Alderaan",
                climate="temperate",
                diameter=12500.0,
                gravity="1 standard",
                orbital_period=364.0,
                population=2000000000.0,
                rotation_period=24.0,
                surface_water=40.0,
                terrain="grasslands, mountains"
            ),
            Planet(
                name="Hoth",
                climate="frozen",
                diameter=7200.0,
                gravity="1.1 standard",
                orbital_period=549.0,
                population=0.0,
                rotation_period=23.0,
                surface_water=100.0,
                terrain="tundra, ice caves, mountain ranges"
            ),
        ]

        # Add starships
        starships = [
            Starship(
                name="X-wing",
                model="T-65 X-wing",
                starship_class="Starfighter",
                manufacturer="Incom Corporation",
                cost_in_credits=149999.0,
                length=12.5,
                crew="1",
                passengers="0",
                max_atmosphering_speed="1050",
                cargo_capacity=110.0,
                consumables="1 week"
            ),
            Starship(
                name="TIE Advanced x1",
                model="Twin Ion Engine Advanced x1",
                starship_class="Starfighter",
                manufacturer="Sienar Fleet Systems",
                cost_in_credits=0.0,
                length=9.2,
                crew="1",
                passengers="0",
                max_atmosphering_speed="1200",
                cargo_capacity=150.0,
                consumables="5 days"
            ),
            Starship(
                name="Millennium Falcon",
                model="YT-1300 light freighter",
                starship_class="Light freighter",
                manufacturer="Corellian Engineering Corporation",
                cost_in_credits=100000.0,
                length=34.37,
                crew="4",
                passengers="6",
                max_atmosphering_speed="1050",
                cargo_capacity=100000.0,
                consumables="2 months"
            ),
        ]

        db.session.add_all(planets + people + starships)
        db.session.commit()
        print("🌱 Seed data added successfully!")

if __name__ == "__main__":
    seed_data()
