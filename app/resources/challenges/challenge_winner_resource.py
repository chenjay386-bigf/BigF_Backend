from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db

from app.models.challenges.challenge import Challenge
from app.models.challenges.challenge_submission import ChallengeSubmission



class ChallengeWinnerResource(Resource):


    # ============================================================
    # SELECT WINNER
    # ============================================================

    @jwt_required()
    def post(self, challenge_id):

        current_user_id = int(
            get_jwt_identity()
        )


        challenge = Challenge.query.get_or_404(
            challenge_id
        )


        # Only creator can choose winner
        if challenge.creator_id != current_user_id:

            return {

                "message":
                "Only the challenge creator can select the winner."

            }, 403



        submissions = ChallengeSubmission.query.filter_by(
            challenge_id=challenge_id
        ).all()



        if not submissions:

            return {

                "message":
                "No submissions found."

            }, 400



        # Sort by votes
        submissions.sort(
            key=lambda x: x.vote_count(),
            reverse=True
        )



        # Reset previous winners

        for submission in submissions:

            submission.is_winner = False

            submission.ranking = None



        # Winner

        winner = submissions[0]

        winner.is_winner = True

        winner.ranking = 1



        # Runner ups

        rank = 2

        for submission in submissions[1:]:

            submission.ranking = rank

            rank += 1



        db.session.commit()



        return {

            "message":
            "Winner selected successfully.",


            "winner": {

                "submission_id":
                winner.id,


                "user_id":
                winner.user_id,


                "username":
                winner.user.username,


                "votes":
                winner.vote_count()

            }

        }, 200





    # ============================================================
    # VIEW WINNER
    # ============================================================

    def get(self, challenge_id):


        challenge = Challenge.query.get_or_404(
            challenge_id
        )


        winner = ChallengeSubmission.query.filter_by(

            challenge_id=challenge_id,

            is_winner=True

        ).first()



        if not winner:

            return {

                "message":
                "Winner has not been selected yet."

            }, 404



        return {


            "challenge_id":
            challenge.id,


            "challenge_title":
            challenge.title,


            "winner": {


                "submission_id":
                winner.id,


                "user_id":
                winner.user_id,


                "username":
                winner.user.username,


                "recipe_id":
                winner.recipe_id,


                "post_id":
                winner.post_id,


                "votes":
                winner.vote_count(),


                "ranking":
                winner.ranking


            }


        }, 200