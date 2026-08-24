from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.post import Post
from app.models.content.media import Media


class MediaResource(Resource):

    @jwt_required()
    def post(self, post_id):

        current_user_id = int(get_jwt_identity())

        post = Post.query.get_or_404(post_id)

        if post.user_id != current_user_id:
            return {
                "message": "You can only add media to your own posts."
            }, 403

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        media = Media(
            post_id=post_id,
            url=data["url"],
            media_type=data.get("media_type", "image"),
            public_id=data.get("public_id", ""),
            position=data.get("position", 1)
        )

        db.session.add(media)
        db.session.commit()

        return {
            "message": "Media added successfully.",
            "media_id": media.id
        }, 201


class MediaDetailResource(Resource):

    def get(self, media_id):

        media = Media.query.get_or_404(media_id)

        return {
            "id": media.id,
            "post_id": media.post_id,
            "url": media.url,
            "media_type": media.media_type,
            "public_id": media.public_id,
            "position": media.position,
            "created_at": (
                media.created_at.isoformat()
                if media.created_at
                else None
            )
        }, 200


    @jwt_required()
    def delete(self, media_id):

        current_user_id = int(get_jwt_identity())

        media = Media.query.get_or_404(media_id)

        if media.post.user_id != current_user_id:
            return {
                "message": "You can only delete your own media."
            }, 403

        db.session.delete(media)
        db.session.commit()

        return {
            "message": "Media deleted successfully."
        }, 200