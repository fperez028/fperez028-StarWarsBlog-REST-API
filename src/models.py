from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
            "favorites": [fav.serialize() for fav in self.favorites],
        }


class Person(db.Model):
    __tablename__ = "person"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(50))
    height: Mapped[float] = mapped_column(Float)
    mass: Mapped[float] = mapped_column(Float)
    skin_color: Mapped[str] = mapped_column(String(50))
    homeworld: Mapped[str] = mapped_column(String(200))

    favorites = relationship("Favorite", back_populates="person")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld,
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    diameter: Mapped[float] = mapped_column(Float)
    gravity: Mapped[str] = mapped_column(String(20))
    orbital_period: Mapped[float] = mapped_column(Float)
    population: Mapped[float] = mapped_column(Float)
    rotation_period: Mapped[float] = mapped_column(Float)
    surface_water: Mapped[float] = mapped_column(Float)
    terrain: Mapped[str] = mapped_column(String(100))

    favorites = relationship("Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
        }


class Starship(db.Model):
    __tablename__ = "starship"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100))
    starship_class: Mapped[str] = mapped_column(String(100))
    manufacturer: Mapped[str] = mapped_column(String(200))
    cost_in_credits: Mapped[float] = mapped_column(Float)
    length: Mapped[float] = mapped_column(Float)
    crew: Mapped[str] = mapped_column(String(50))
    passengers: Mapped[str] = mapped_column(String(50))
    max_atmosphering_speed: Mapped[str] = mapped_column(String(50))
    cargo_capacity: Mapped[float] = mapped_column(Float)
    consumables: Mapped[str] = mapped_column(String(50))

    favorites = relationship("Favorite", back_populates="starship")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
        }


class Favorite(db.Model):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    starship_id: Mapped[int] = mapped_column(ForeignKey("starship.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "person_id", name="uq_user_person"),
        UniqueConstraint("user_id", "planet_id", name="uq_user_planet"),
        UniqueConstraint("user_id", "starship_id", name="uq_user_starship"),
    )

    user = relationship("User", back_populates="favorites")
    person = relationship("Person", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    starship = relationship("Starship", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person": self.person.serialize() if self.person else None,
            "planet": self.planet.serialize() if self.planet else None,
            "starship": self.starship.serialize() if self.starship else None,
        }
