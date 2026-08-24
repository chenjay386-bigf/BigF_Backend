from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.post import Post
from app.models.content.reshare import Reshare


class ReshareResource(Resource):

    @jwt_required()
    def post(self, post_id):

        current_user_id = get_jwt_identity()

        Post.query.get_or_404(post_id)

        existing = Reshare.query.filter_by(
            user_id=current_user_id,
            post_id=post_id
        ).first()

        if existing:
            return {
                "message": "You have already reshared this post."
            }, 409

        reshare = Reshare(
            user_id=current_user_id,
            post_id=post_id
        )

        db.session.add(reshare)
        db.session.commit()

        return {
            "message": "Post reshared successfully."
        }, 201


class RemoveReshareResource(Resource):

    @jwt_required()
    def delete(self, post_id):

        current_user_id = get_jwt_identity()

        reshare = Reshare.query.filter_by(
            user_id=current_user_id,
            post_id=post_id
        ).first()

        if not reshare:
            return {
                "message": "You have not reshared this post."
            }, 404

        db.session.delete(reshare)
        db.session.commit()

        return {
            "message": "Reshare removed successfully."
        }, 200


class PostResharesResource(Resource):

    def get(self, post_id):

        Post.query.get_or_404(post_id)

        reshares = Reshare.query.filter_by(
            post_id=post_id
        ).all()

        reshare_list = []

        for reshare in reshares:

            reshare_list.append({
                "id": reshare.id,
                "user": {
                    "id": reshare.user.id,
                    "username": reshare.user.username
                },
                "created_at": reshare.created_at.isoformat()
            })

        return {
            "count": len(reshare_list),
            "reshares": reshare_list
        }, 200
        return {
            "count": len(reshare_list),
            "reshares": reshare_list
        }, 200