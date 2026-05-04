"""User model."""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import uuid


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    tasks_created = db.relationship("Task", foreign_keys="Task.creator_id", backref="creator")
    tasks_assigned = db.relationship("Task", foreign_keys="Task.assignee_id", backref="assignee")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
