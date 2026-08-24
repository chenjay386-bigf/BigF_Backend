from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db

from app.models.challenges.challenge import Challenge
from app.models.challenges.challenge_submission import ChallengeSubmission


# ============================================================
# TIKTOK URL VALIDATION
# ============================================================

def is_valid_tiktok_url(url):
    """
    Accept normal TikTok video/profile URLs.

    Examples:
        https://www.tiktok.com/@username/video/123456789
        https://vm.tiktok.com/ABC123/
        https://vt.tiktok.com/ABC123/
    """

    if not url:
        return False

    if not isinstance(url, str):
        return False

    url = url.strip().lower()

    return (
        url.startswith("https://www.tiktok.com/")
        or url.startswith("https://tiktok.com/")
        or url.startswith("https://vm.tiktok.com/")
        or url.startswith("https://vt.tiktok.com/")
    )


# ============================================================
# SERIALIZE SUBMISSION
# ============================================================

def serialize_submission(submission):

    return {
        "id": submission.id,

        "challenge_id": submission.challenge_id,

        "user": {
            "id": submission.user.id,
            "username": submission.user.username,
            "profile_image": (
                submission.user.profile.profile_image
                if submission.user.profile
                else None
            )
        },

        "recipe_id": submission.recipe_id,

        "post_id": submission.post_id,

        "tiktok_url": submission.tiktok_url,

        "description": submission.description,

        "status": submission.status,

        "moderation_note": submission.moderation_note,

        "votes": submission.vote_count(),

        "is_winner": submission.is_winner,

        "ranking": submission.ranking,

        "created_at": submission.created_at.isoformat(),

        "updated_at": submission.updated_at.isoformat()
        if submission.updated_at
        else None
    }


# ============================================================
# CREATE CHALLENGE SUBMISSION
# ============================================================

class ChallengeSubmissionResource(Resource):

    @jwt_required()
    def post(self, challenge_id):

        current_user_id = int(
            get_jwt_identity()
        )

        challenge = Challenge.query.get_or_404(
            challenge_id
        )

        # ----------------------------------------------------
        # ONLY ACTIVE CHALLENGES
        # ----------------------------------------------------

        if challenge.status != "active":

            return {
                "message": "This challenge is not active."
            }, 400

        data = request.get_json()

        if not data:

            return {
                "message": "Request body is required."
            }, 400

        # ----------------------------------------------------
        # PREVENT DUPLICATE SUBMISSION
        # ----------------------------------------------------

        existing_submission = ChallengeSubmission.query.filter_by(
            challenge_id=challenge_id,
            user_id=current_user_id
        ).first()

        if existing_submission:

            return {
                "message": "You have already joined this challenge.",
                "submission_id": existing_submission.id,
                "status": existing_submission.status
            }, 409

        # ----------------------------------------------------
        # TIKTOK URL
        # ----------------------------------------------------

        tiktok_url = data.get("tiktok_url")

        if tiktok_url:

            tiktok_url = tiktok_url.strip()

            if not is_valid_tiktok_url(tiktok_url):

                return {
                    "message": "Please provide a valid TikTok URL."
                }, 400

        # ----------------------------------------------------
        # CREATE SUBMISSION
        # ----------------------------------------------------

        submission = ChallengeSubmission(

            challenge_id=challenge_id,

            user_id=current_user_id,

            recipe_id=data.get(
                "recipe_id"
            ),

            post_id=data.get(
                "post_id"
            ),

            tiktok_url=tiktok_url,

            description=data.get(
                "description"
            ),

            # New submissions require moderation
            status="pending",

            moderation_note=None

        )

        db.session.add(
            submission
        )

        db.session.commit()

        return {

            "message":
                "Challenge submission created and is awaiting moderation.",

            "submission_id":
                submission.id,

            "status":
                submission.status

        }, 201


# ============================================================
# SINGLE SUBMISSION
# ============================================================

class ChallengeSubmissionDetailResource(Resource):

    # --------------------------------------------------------
    # GET SINGLE SUBMISSION
    # --------------------------------------------------------

    def get(self, submission_id):

        submission = ChallengeSubmission.query.get_or_404(
            submission_id
        )

        return serialize_submission(
            submission
        ), 200

    # --------------------------------------------------------
    # DELETE OWN SUBMISSION
    # --------------------------------------------------------

    @jwt_required()
    def delete(self, submission_id):

        current_user_id = int(
            get_jwt_identity()
        )

        submission = ChallengeSubmission.query.get_or_404(
            submission_id
        )

        if submission.user_id != current_user_id:

            return {
                "message":
                    "You can only delete your own submission."
            }, 403

        db.session.delete(
            submission
        )

        db.session.commit()

        return {
            "message":
                "Challenge submission deleted successfully."
        }, 200


# ============================================================
# ALL APPROVED SUBMISSIONS FOR ONE CHALLENGE
# ============================================================

class ChallengeSubmissionsResource(Resource):

    def get(self, challenge_id):

        Challenge.query.get_or_404(
            challenge_id
        )

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # Only APPROVED submissions appear publicly.
        # Pending/rejected submissions cannot be voted on.
        # ----------------------------------------------------

        submissions = ChallengeSubmission.query.filter_by(

            challenge_id=challenge_id,

            status="approved"

        ).all()

        submission_list = []

        for submission in submissions:

            submission_list.append(
                serialize_submission(
                    submission
                )
            )

        # ----------------------------------------------------
        # SORT HIGHEST VOTES FIRST
        # ----------------------------------------------------

        submission_list.sort(

            key=lambda x: x["votes"],

            reverse=True

        )

        return {

            "challenge_id":
                challenge_id,

            "participants":
                len(submission_list),

            "submissions":
                submission_list

        }, 200


# ============================================================
# ADMIN - PENDING SUBMISSIONS
# ============================================================

class AdminPendingChallengeSubmissionsResource(Resource):

    @jwt_required()
    def get(self):

        # ----------------------------------------------------
        # TODO:
        # Replace this with your existing admin permission
        # check if you already have one.
        # ----------------------------------------------------

        current_user_id = int(
            get_jwt_identity()
        )

        # IMPORTANT:
        # Put your existing admin authorization here.
        #
        # Example:
        #
        # user = User.query.get(current_user_id)
        #
        # if not user.is_admin:
        #     return {
        #         "message": "Admin access required."
        #     }, 403

        submissions = ChallengeSubmission.query.filter_by(

            status="pending"

        ).order_by(

            ChallengeSubmission.created_at.asc()

        ).all()

        return {

            "count":
                len(submissions),

            "submissions": [

                serialize_submission(
                    submission
                )

                for submission in submissions

            ]

        }, 200


# ============================================================
# ADMIN - APPROVE SUBMISSION
# ============================================================

class AdminApproveChallengeSubmissionResource(Resource):

    @jwt_required()
    def patch(self, submission_id):

        # ----------------------------------------------------
        # TODO:
        # Replace this with your existing admin permission
        # check.
        # ----------------------------------------------------

        submission = ChallengeSubmission.query.get_or_404(
            submission_id
        )

        if submission.status != "pending":

            return {

                "message":
                    "Only pending submissions can be approved.",

                "status":
                    submission.status

            }, 400

        submission.status = "approved"

        submission.moderation_note = None

        db.session.commit()

        return {

            "message":
                "Challenge submission approved.",

            "submission":
                serialize_submission(
                    submission
                )

        }, 200


# ============================================================
# ADMIN - REJECT SUBMISSION
# ============================================================

class AdminRejectChallengeSubmissionResource(Resource):

    @jwt_required()
    def patch(self, submission_id):

        # ----------------------------------------------------
        # TODO:
        # Replace this with your existing admin permission
        # check.
        # ----------------------------------------------------

        submission = ChallengeSubmission.query.get_or_404(
            submission_id
        )

        if submission.status != "pending":

            return {

                "message":
                    "Only pending submissions can be rejected.",

                "status":
                    submission.status

            }, 400

        data = request.get_json() or {}

        moderation_note = data.get(
            "moderation_note"
        )

        submission.status = "rejected"

        submission.moderation_note = moderation_note

        db.session.commit()

        return {

            "message":
                "Challenge submission rejected.",

            "submission":
                serialize_submission(
                    submission
                )

        }, 200