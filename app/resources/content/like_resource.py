
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.post import Post
from app.models.content.like import Like


class LikeResource(Resource):

    @jwt_required()
    def post(self, post_id):

        current_user_id = get_jwt_identity()

        # Make sure the post exists
        Post.query.get_or_404(post_id)

        # Check if the user already liked the post
        existing = Like.query.filter_by(
            user_id=current_user_id,
            post_id=post_id
        ).first()

        if existing:
            return {
                "message": "You have already liked this post."
            }, 409

        like = Like(
            user_id=current_user_id,
            post_id=post_id
        )

        db.session.add(like)
        db.session.commit()

        return {
            "message": "Post liked successfully."
        }, 201


class UnlikeResource(Resource):

    @jwt_required()
    def delete(self, post_id):

        current_user_id = get_jwt_identity()

        like = Like.query.filter_by(
            user_id=current_user_id,
            post_id=post_id
        ).first()

        if not like:
            return {
                "message": "You have not liked this post."
            }, 404

        db.session.delete(like)
        db.session.commit()

        return {
            "message": "Post unliked successfully."
        }, 200


class PostLikesResource(Resource):

    def get(self, post_id):

        # Make sure the post exists
        Post.query.get_or_404(post_id)

        likes = Like.query.filter_by(
            post_id=post_id
        ).all()

        like_list = []

        for like in likes:

            like_list.append({
                "id": like.id,
                "user": {
                    "id": like.user.id,
                    "username": like.user.username
                },
                "created_at": (
                    like.created_at.isoformat()
                    if like.created_at
                    else None
                )
            })

        return {
            "count": len(like_list),
            "likes": like_list
        }, 200
