from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64), index=True, nullable=False)
    model = db.Column(db.String(64), index=True, nullable=False)
    year = db.Column(db.Integer, index=True, nullable=False)
    price = db.Column(db.Float, index=True, nullable=False)
    image_filename = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vehicle {self.make} {self.model} {self.year} - ${self.price}>'

# Create an admin user for demonstration purposes
# FIXMEE: In a real application, handle user creation securely
admin_user = User(
    id = 1,
    username = 'admin',
    password_hash = generate_password_hash('password')
)