from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.user.user import User
from app.models.user.profile import Profile


class RegisterResource(Resource):

    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {
                "message": "Username, email and password are required."
            }, 400

        if User.query.filter_by(username=username).first():
            return {
                "message": "Username already exists."
            }, 409

        if User.query.filter_by(email=email).first():
            return {
                "message": "Email already exists."
            }, 409

        user = User(
            username=username,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        profile = Profile(
            user_id=user.id,
            display_name=username
        )

        db.session.add(profile)
        db.session.commit()

        return {
            "message": "Registration successful."
        }, 201


class LoginResource(Resource):

    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {
                "message": "Email and password are required."
            }, 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return {
                "message": "Invalid credentials."
            }, 401

        if not user.check_password(password):
            return {
                "message": "Invalid credentials."
            }, 401

        user.update_last_login()
        db.session.commit()

        # JWT subject must be a string
        access_token = create_access_token(
            identity=str(user.id)
        )

        return {
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }, 200


class MeResource(Resource):

    @jwt_required()
    def get(self):

        # Convert JWT string identity back to integer database ID
        user_id = int(get_jwt_identity())

        user = User.query.get_or_404(user_id)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "profile": {
                "display_name": user.profile.display_name,
                "bio": user.profile.bio,
                "profile_image": user.profile.profile_image
            }
        }, 200


class ChangePasswordResource(Resource):

    @jwt_required()
    def patch(self):

        data = request.get_json()

        current_password = data.get("current_password")
        new_password = data.get("new_password")

        user_id = int(get_jwt_identity())

        user = User.query.get_or_404(user_id)

        if not user.check_password(current_password):
            return {
                "message": "Current password is incorrect."
            }, 400

        user.set_password(new_password)

        db.session.commit()

        return {
            "message": "Password updated successfully."
        }, 200


class AdminLoginResource(Resource):
    def post(self):
        data = request.get_json() or {}
        passcode = data.get("passcode")

        # Validate admin passcode
        if passcode == "admin123" or passcode == "BIGF2026":
            response = make_response(jsonify({
                "success": True, 
                "message": "Admin logged in successfully"
            }), 200)

            # Set the secure HttpOnly cookie for the admin session
            response.set_cookie(
                key="bigf_admin_session",
                value="secure_admin_token_xyz",
                httponly=True,
                secure=False,      # False for local HTTP development
                samesite="Lax",
                max_age=86400      # 1 day expiration
            )
            return response

        return {"success": False, "message": "Incorrect admin passcode"}, 401