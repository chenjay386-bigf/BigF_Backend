from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.user.user import User
from app.models.user.profile import Profile
from app.schemas.user.profile_schema import profile_schema


class MyProfileResource(Resource):

    @jwt_required()
    def get(self):

        user = User.query.get_or_404(
            get_jwt_identity()
        )

        return profile_schema.dump(user.profile), 200

    @jwt_required()
    def put(self):

        user = User.query.get_or_404(
            get_jwt_identity()
        )

        data = request.get_json()

        profile = user.profile

        if not profile:
            profile = Profile(
                user_id=user.id,
                display_name=user.username
            )
            db.session.add(profile)

        profile.display_name = data.get(
            "display_name",
            profile.display_name
        )
        profile.bio = data.get(
            "bio",
            profile.bio
        )
        profile.profile_image = data.get(
            "profile_image",
            profile.profile_image
        )

        db.session.commit()

        return profile_schema.dump(profile), 200


class UserProfileResource(Resource):

    def get(self, user_id):

        user = User.query.get_or_404(user_id)

        if not user.profile:
            return {
                "message": "Profile not found."
            }, 404

        return profile_schema.dump(user.profile), 200