from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db

from app.models.challenges.challenge_submission import ChallengeSubmission
from app.models.challenges.challenge_vote import ChallengeVote



# ============================================================
# VOTE ON CHALLENGE SUBMISSION
# ============================================================

class ChallengeVoteResource(Resource):


    # --------------------------------------------------------
    # ADD VOTE
    # --------------------------------------------------------

    @jwt_required()
    def post(self, submission_id):

        current_user_id = int(
            get_jwt_identity()
        )


        submission = ChallengeSubmission.query.get_or_404(
            submission_id
        )


        # Prevent voting for yourself
        if submission.user_id == current_user_id:

            return {

                "message":
                "You cannot vote for your own submission."

            }, 403



        # Prevent duplicate votes

        existing_vote = ChallengeVote.query.filter_by(

            submission_id=submission_id,

            user_id=current_user_id

        ).first()



        if existing_vote:

            return {

                "message":
                "You have already voted for this submission."

            }, 409



        vote = ChallengeVote(

            submission_id=submission_id,

            user_id=current_user_id

        )


        db.session.add(vote)

        db.session.commit()



        return {


            "message":
            "Vote added successfully.",


            "submission_id":
            submission_id,


            "vote_id":
            vote.id

        }, 201





    # --------------------------------------------------------
    # REMOVE VOTE
    # --------------------------------------------------------

    @jwt_required()
    def delete(self, submission_id):

        current_user_id = int(
            get_jwt_identity()
        )


        vote = ChallengeVote.query.filter_by(

            submission_id=submission_id,

            user_id=current_user_id

        ).first()



        if not vote:

            return {

                "message":
                "You have not voted for this submission."

            },404



        db.session.delete(vote)

        db.session.commit()



        return {


            "message":
            "Vote removed successfully."

        },200





# ============================================================
# VIEW SUBMISSION VOTES
# ============================================================

class ChallengeSubmissionVotesResource(Resource):


    def get(self, submission_id):


        submission = ChallengeSubmission.query.get_or_404(
            submission_id
        )



        votes = ChallengeVote.query.filter_by(

            submission_id=submission_id

        ).all()



        voters = []



        for vote in votes:

            voters.append({

                "user_id":
                vote.user.id,


                "username":
                vote.user.username,


                "voted_at":
                vote.created_at.isoformat()

            })



        return {


            "submission_id":
            submission.id,


            "total_votes":
            len(votes),


            "voters":
            voters

        },200