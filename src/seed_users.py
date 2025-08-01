import random
from src.app import app
from src.models import db, User, Favorite, Planet, Person, Starship

def seed_users_and_favorites():
    with app.app_context():
        # Optional: Clear existing users and favorites
        db.session.query(Favorite).delete()
        db.session.query(User).delete()

        # Create users
        users = [
            User(username="luke_skywalker"),
            User(username="leia_organa"),
            User(username="vader")
        ]
        db.session.add_all(users)
        db.session.commit()

        # Retrieve seeded content
        planets = Planet.query.all()
        people = Person.query.all()
        starships = Starship.query.all()

        all_items = planets + people + starships

        def create_favorite(user, item):
            if isinstance(item, Planet):
                return Favorite(user_id=user.id, planet_id=item.id)
            elif isinstance(item, Person):
                return Favorite(user_id=user.id, person_id=item.id)
            elif isinstance(item, Starship):
                return Favorite(user_id=user.id, starship_id=item.id)
            return None

        # Assign 2–3 random favorites per user
        for user in users:
            chosen_items = random.sample(all_items, k=random.randint(2, 3))
            favorites = [create_favorite(user, item) for item in chosen_items]
            db.session.add_all(favorites)

        db.session.commit()
        print("🌱 Seed users and random favorites added successfully!")

if __name__ == "__main__":
    seed_users_and_favorites()
