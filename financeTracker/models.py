from financeTracker import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.Datetime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"User: {self.username}, Joined: {self.date_created}"