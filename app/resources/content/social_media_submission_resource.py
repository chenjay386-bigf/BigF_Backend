from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.social_media_submission import SocialMediaSubmission


class SocialMediaSubmissionResource(Resource):

    @jwt_required()
    def post(self):

        current_user_id = int(get_jwt_identity())

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        submission = SocialMediaSubmission(
            user_id=current_user_id,
            post_id=data.get("post_id"),
            platform=data.get("platform"),
            url=data.get("url"),
            status=data.get("status", "pending")
        )

        db.session.add(submission)
        db.session.commit()

        return {
            "message": "Social media submission created successfully.",
            "submission_id": submission.id
        }, 201



class SocialMediaSubmissionDetailResource(Resource):

    def get(self, submission_id):

        submission = SocialMediaSubmission.query.get_or_404(
            submission_id
        )

        return {
            "id": submission.id,
            "user_id": submission.user_id,
            "post_id": submission.post_id,
            "platform": submission.platform,
            "url": submission.url,
            "status": submission.status,
            "created_at": (
                submission.created_at.isoformat()
                if submission.created_at
                else None
            )
        }, 200


    @jwt_required()
    def delete(self, submission_id):

        current_user_id = int(get_jwt_identity())

        submission = SocialMediaSubmission.query.get_or_404(
            submission_id
        )

        if submission.user_id != current_user_id:
            return {
                "message": "You can only delete your own submissions."
            }, 403


        db.session.delete(submission)
        db.session.commit()

        return {
            "message": "Submission deleted successfully."
        }, 200



class UserSocialMediaSubmissionsResource(Resource):

    @jwt_required()
    def get(self):

        current_user_id = int(get_jwt_identity())

        submissions = SocialMediaSubmission.query.filter_by(
            user_id=current_user_id
        ).all()


        submission_list = []

        for submission in submissions:

            submission_list.append({

                "id": submission.id,

                "post_id": submission.post_id,

                "platform": submission.platform,

                "url": submission.url,

                "status": submission.status,

                "created_at": (
                    submission.created_at.isoformat()
                    if submission.created_at
                    else None
                )
            })


        return submission_list, 200