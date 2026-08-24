
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.post import Post


class PostResource(Resource):

    def get(self):

        posts = Post.query.filter_by(
            status="published"
        ).all()

        post_list = []

        for post in posts:

            post_list.append({
                "id": post.id,
                "caption": post.caption,
                "status": post.status,
                "recipe_id": post.recipe_id,
                "user": {
                    "id": post.user.id,
                    "username": post.user.username
                },
                "created_at": post.created_at.isoformat()
                    if post.created_at else None,
                "updated_at": post.updated_at.isoformat()
                    if post.updated_at else None
            })

        return post_list, 200

    @jwt_required()
    def post(self):

        current_user_id = int(get_jwt_identity())

        data = request.get_json() or {}

        post = Post(
            user_id=current_user_id,
            recipe_id=data.get("recipe_id"),
            caption=data.get("caption"),
            status=data.get("status", "published")
        )

        db.session.add(post)
        db.session.commit()

        return {
            "message": "Post created successfully.",
            "post_id": post.id
        }, 201


class PostDetailResource(Resource):

    def get(self, post_id):

        post = Post.query.get_or_404(post_id)

        return {
            "id": post.id,
            "caption": post.caption,
            "status": post.status,
            "recipe_id": post.recipe_id,
            "user": {
                "id": post.user.id,
                "username": post.user.username
            },
            "created_at": post.created_at.isoformat()
                if post.created_at else None,
            "updated_at": post.updated_at.isoformat()
                if post.updated_at else None
        }, 200

    @jwt_required()
    def put(self, post_id):

        current_user_id = int(get_jwt_identity())

        post = Post.query.get_or_404(post_id)

        if post.user_id != current_user_id:
            return {
                "message": "You can only update your own posts."
            }, 403

        data = request.get_json() or {}

        post.caption = data.get(
            "caption",
            post.caption
        )

        post.status = data.get(
            "status",
            post.status
        )

        db.session.commit()

        return {
            "message": "Post updated successfully."
        }, 200

    @jwt_required()
    def delete(self, post_id):

        current_user_id = int(get_jwt_identity())

        post = Post.query.get_or_404(post_id)

        if post.user_id != current_user_id:
            return {
                "message": "You can only delete your own posts."
            }, 403

        db.session.delete(post)
        db.session.commit()

        return {
            "message": "Post deleted successfully."
        }, 200