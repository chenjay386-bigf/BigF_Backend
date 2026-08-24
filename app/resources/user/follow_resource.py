from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.user.user import User
from app.models.user.follow import Follow
from app.schemas.user.follow_schema import (
    follow_schema,
    follows_schema
)


class FollowResource(Resource):

    @jwt_required()
    def post(self, user_id):

        current_user_id = get_jwt_identity()

        if current_user_id == user_id:
            return {
                "message": "You cannot follow yourself."
            }, 400

        target_user = User.query.get_or_404(user_id)

        existing = Follow.query.filter_by(
            follower_id=current_user_id,
            following_id=user_id
        ).first()

        if existing:
            return {
                "message": "You are already following this user."
            }, 409

        follow = Follow(
            follower_id=current_user_id,
            following_id=user_id
        )

        db.session.add(follow)
        db.session.commit()

        return follow_schema.dump(follow), 201

    @jwt_required()
    def delete(self, user_id):

        current_user_id = get_jwt_identity()

        follow = Follow.query.filter_by(
            follower_id=current_user_id,
            following_id=user_id
        ).first()

        if not follow:
            return {
                "message": "You are not following this user."
            }, 404

        db.session.delete(follow)
        db.session.commit()

        return {
            "message": "Unfollowed successfully."
        }, 200


class FollowersResource(Resource):

    def get(self, user_id):

        user = User.query.get_or_404(user_id)

        followers = Follow.query.filter_by(
            following_id=user_id
        ).all()

        return follows_schema.dump(followers), 200


class FollowingResource(Resource):

    def get(self, user_id):

        user = User.query.get_or_404(user_id)

        following = Follow.query.filter_by(
            follower_id=user_id
        ).all()

        return follows_schema.dump(following), 200