
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.post import Post
from app.models.content.comment import Comment


class CommentResource(Resource):

    def get(self, post_id):

        Post.query.get_or_404(post_id)

        comments = Comment.query.filter_by(
            post_id=post_id
        ).order_by(
            Comment.created_at.asc()
        ).all()

        comment_list = []

        for comment in comments:

            comment_list.append({
                "id": comment.id,
                "content": comment.content,
                "user": {
                    "id": comment.user.id,
                    "username": comment.user.username
                },
                "created_at": (
                    comment.created_at.isoformat()
                    if comment.created_at
                    else None
                )
            })

        return comment_list, 200

    @jwt_required()
    def post(self, post_id):

        current_user_id = int(get_jwt_identity())

        Post.query.get_or_404(post_id)

        data = request.get_json() or {}

        content = data.get("content")

        if not content:
            return {
                "message": "Comment content is required."
            }, 400

        comment = Comment(
            user_id=current_user_id,
            post_id=post_id,
            content=content
        )

        db.session.add(comment)
        db.session.commit()

        return {
            "message": "Comment added successfully.",
            "comment_id": comment.id
        }, 201


class CommentDetailResource(Resource):

    @jwt_required()
    def put(self, comment_id):

        current_user_id = int(get_jwt_identity())

        comment = Comment.query.get_or_404(comment_id)

        if comment.user_id != current_user_id:
            return {
                "message": "You can only edit your own comments."
            }, 403

        data = request.get_json() or {}

        content = data.get("content")

        if not content:
            return {
                "message": "Comment content is required."
            }, 400

        comment.content = content

        db.session.commit()

        return {
            "message": "Comment updated successfully."
        }, 200

    @jwt_required()
    def delete(self, comment_id):

        current_user_id = int(get_jwt_identity())

        comment = Comment.query.get_or_404(comment_id)

        if comment.user_id != current_user_id:
            return {
                "message": "You can only delete your own comments."
            }, 403

        db.session.delete(comment)
        db.session.commit()

        return {
            "message": "Comment deleted successfully."
        }, 200
