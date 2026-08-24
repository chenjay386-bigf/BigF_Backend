from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.challenges.challenge_submission import ChallengeSubmission


# ============================================================
# ADMIN CHECK
# ============================================================

def require_admin():
    """
    Temporary/simple admin check.

    Replace the inside of this function with your existing
    admin permission logic if your User model already has
    an is_admin field or another admin-role system.
    """

    from app.models.user.user import User

    current_user_id = int(get_jwt_identity())

    user = User.query.get(current_user_id)

    if not user:
        return None, (
            {
                "message": "User not found."
            },
            404
        )

    # --------------------------------------------------------
    # USE YOUR EXISTING ADMIN FIELD
    # --------------------------------------------------------

    if not getattr(user, "is_admin", False):
        return None, (
            {
                "message": "Admin access required."
            },
            403
        )

    return user, None


# ============================================================
# SERIALIZE
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

        "created_at": (
            submission.created_at.isoformat()
            if submission.created_at
            else None
        ),

        "updated_at": (
            submission.updated_at.isoformat()
            if submission.updated_at
            else None
        )
    }


# ============================================================
# ADMIN - LIST PENDING SUBMISSIONS
# ============================================================

class ChallengeSubmissionModerationListResource(Resource):

    @jwt_required()
    def get(self):

        _, error = require_admin()

        if error:
            return error

        submissions = (
            ChallengeSubmission.query
            .filter_by(status="pending")
            .order_by(
                ChallengeSubmission.created_at.asc()
            )
            .all()
        )

        return {
            "count": len(submissions),

            "submissions": [
                serialize_submission(submission)
                for submission in submissions
            ]
        }, 200


# ============================================================
# ADMIN - MODERATE SUBMISSION
# ============================================================

class ChallengeSubmissionModerationResource(Resource):

    @jwt_required()
    def get(self, submission_id):

        _, error = require_admin()

        if error:
            return error

        submission = (
            ChallengeSubmission.query
            .get_or_404(submission_id)
        )

        return {
            "submission": serialize_submission(
                submission
            )
        }, 200

    @jwt_required()
    def put(self, submission_id):

        _, error = require_admin()

        if error:
            return error

        submission = (
            ChallengeSubmission.query
            .get_or_404(submission_id)
        )

        # ----------------------------------------------------
        # REQUEST DATA
        # ----------------------------------------------------

        data = request.get_json() or {}

        action = data.get("action")

        moderation_note = data.get(
            "moderation_note"
        )

        # ----------------------------------------------------
        # VALID ACTIONS
        # ----------------------------------------------------

        if action not in [
            "approve",
            "reject"
        ]:

            return {
                "message": (
                    "Invalid moderation action. "
                    "Use 'approve' or 'reject'."
                )
            }, 400

        # ----------------------------------------------------
        # ONLY PENDING SUBMISSIONS
        # ----------------------------------------------------

        if submission.status != "pending":

            return {
                "message": (
                    "Only pending submissions "
                    "can be moderated."
                ),
                "status": submission.status
            }, 400

        # ----------------------------------------------------
        # APPROVE
        # ----------------------------------------------------

        if action == "approve":

            submission.status = "approved"

            submission.moderation_note = None

            db.session.commit()

            return {
                "message": (
                    "Challenge submission "
                    "approved successfully."
                ),

                "submission": serialize_submission(
                    submission
                )
            }, 200

        # ----------------------------------------------------
        # REJECT
        # ----------------------------------------------------

        if action == "reject":

            submission.status = "rejected"

            submission.moderation_note = (
                moderation_note
            )

            db.session.commit()

            return {
                "message": (
                    "Challenge submission "
                    "rejected successfully."
                ),

                "submission": serialize_submission(
                    submission
                )
            }, 200