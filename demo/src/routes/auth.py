"""Authentication routes."""

from flask import Blueprint, request, jsonify
from models.user import User
from app import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if user and user.check_password(data.get("password")):
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"error": "Email already registered"}), 400
    user = User(email=data["email"], name=data["name"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registration successful", "user_id": user.id}), 201
