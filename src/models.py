from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relación con People (muchos a muchos)
    favorites_people = relationship('People', secondary='user_favorites_people', back_populates='users')

    # Relación con Planet (muchos a muchos)
    favorites_planets = relationship('Planet', secondary='user_favorites_planets', back_populates='users')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active
        }

class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    locations: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    dimensions: Mapped[str] = mapped_column(nullable=False)
    weapons: Mapped[str] = mapped_column(nullable=False)

    # Relación con User (muchos a muchos)
    users = relationship('User', secondary='user_favorites_people', back_populates='favorites_people')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "locations": self.locations,
            "gender": self.gender,
            "dimensions": self.dimensions,
            "weapons": self.weapons,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    appearances: Mapped[str] = mapped_column(nullable=False)

    # Relación con User (muchos a muchos)
    users = relationship('User', secondary='user_favorites_planets', back_populates='favorites_planets')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "appearances": self.appearances,
        }

# Relación muchos a muchos entre User y People a través de la tabla intermedia
user_favorites_people = db.Table(
    'user_favorites_people',
    db.Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('people_id', Integer, ForeignKey('people.id', ondelete='CASCADE'), primary_key=True)
)

# Relación muchos a muchos entre User y Planet a través de la tabla intermedia
user_favorites_planets = db.Table(
    'user_favorites_planets',
    db.Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('planet_id', Integer, ForeignKey('planet.id', ondelete='CASCADE'), primary_key=True)
)