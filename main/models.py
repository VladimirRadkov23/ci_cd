from sqlalchemy import Constraint, Nullable

from . app import db
from typing import Dict, Any


class Clients(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.Integer, nullable=True)
    car_number = db.Column(db.String(20), nullable=True)

    client_id = db.relationship("ClientParking", back_populates="client")

    def __repr__(self):
        return f"Number {self.car_number}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Parking(db.Model):
    __tablename__ = 'parking'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    opened = db.Column(db.Boolean, nullable=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    client_parking = db.relationship("ClientParking", back_populates="parking")

    def __repr__(self):
        return f"Пользователь {self.address} {self.count_places}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=False)
    time_on = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)
    unique_client_parking = [db.UniqueConstraint(client_id, parking_id)]

    client = db.relationship("Clients", back_populates="client_id")
    parking = db.relationship("Parking", back_populates="client_parking")

    def __repr__(self):
        return f"Пользователь {self.time_on} {self.time_out}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}
