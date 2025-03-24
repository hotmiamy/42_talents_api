from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    linkedin_profile = db.Column(db.String(200))
    github_profile = db.Column(db.String(200))
    skills = db.Column(db.JSONB)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)
    idioms = db.Column(db.JSON)
    bio = db.Column(db.Text)
    open_to_work = db.Column(db.Boolean, default=True)
    cv_filename = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<profile {self.name}>'