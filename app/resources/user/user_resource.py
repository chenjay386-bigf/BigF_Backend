from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from flask import request

from app.extensions import db

from app.models.user.user import User


class UserResource(Resource):

    # GET ALL USERS
    def get(self):

        users = User.query.all()

        user_list = []

        for user in users:

            user_list.append({

                "id": user.id,

                "username": user.username,

                "email": user.email

            })


        return user_list, 200



class UserDetailResource(Resource):

    # GET SINGLE USER
    def get(self, user_id):

        user = User.query.get_or_404(
            user_id
        )


        return {

            "id": user.id,

            "username": user.username,

            "email": user.email

        }, 200



    # UPDATE CURRENT USER
    @jwt_required()
    def put(self, user_id):

        current_user_id = get_jwt_identity()


        if current_user_id != user_id:

            return {

                "message":
                "You can only update your own account."

            }, 403



        user = User.query.get_or_404(
            user_id
        )


        data = request.get_json()


        user.username = data.get(
            "username",
            user.username
        )


        user.email = data.get(
            "email",
            user.email
        )


        db.session.commit()


        return {

            "message":
            "User updated successfully."

        }, 200



    # DELETE USER
    @jwt_required()
    def delete(self, user_id):

        current_user_id = get_jwt_identity()


        if current_user_id != user_id:

            return {

                "message":
                "You can only delete your own account."

            }, 403



        user = User.query.get_or_404(
            user_id
        )


        db.session.delete(user)

        db.session.commit()


        return {

            "message":
            "User deleted successfully."

        }, 200