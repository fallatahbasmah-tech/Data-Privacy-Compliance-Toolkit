from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

def now(): return datetime.now(timezone.utc)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    assessments = db.relationship('Assessment', backref='owner', cascade='all, delete-orphan')
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    organization = db.Column(db.String(160), nullable=False)
    industry = db.Column(db.String(80), nullable=False)
    employees = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime, default=now, nullable=False)
    responses = db.relationship('Response', backref='assessment', cascade='all, delete-orphan')

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    code = db.Column(db.String(40), nullable=False)
    answer = db.Column(db.String(12), nullable=False)
    __table_args__ = (db.UniqueConstraint('assessment_id','code', name='unique_assessment_question'),)
