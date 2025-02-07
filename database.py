# Database setup
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # Skills Dev, Psyche, Health
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)