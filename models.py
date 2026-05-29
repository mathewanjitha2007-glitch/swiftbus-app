from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# User Table - stores all registered users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Bus Table - stores all buses
class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_name = db.Column(db.String(100), nullable=False)
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    from_city = db.Column(db.String(50), nullable=False)
    to_city = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.String(20), nullable=False)
    arrival_time = db.Column(db.String(20), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    travel_date = db.Column(db.String(20), nullable=False)

# Booking Table - stores all ticket bookings
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')

    user = db.relationship('User', backref='bookings')
    bus = db.relationship('Bus', backref='bookings')
