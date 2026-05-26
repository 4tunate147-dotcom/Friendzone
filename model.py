from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

db = SQLAlchemy()

class FriendList(db.Model):
    __tablename__ = 'friendlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    profile_pix = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())