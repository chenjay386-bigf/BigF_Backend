from datetime import datetime, timezone

from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db

from app.models.challenges.challenge import Challenge
from app.models.challenges.challenge_submission import ChallengeSubmission
from app.models.challenges.challenge_reward import ChallengeReward



# ============================================================
# ASSIGN WINNER / CREATE REWARD
# ============================================================

class ChallengeRewardResource(Resource):


    @jwt_required()
    def post(self, challenge_id):

        current_user_id = int(
            get_jwt_identity()
        )


        challenge = Challenge.query.get_or_404(
            challenge_id
        )


        # Only creator can assign winner
        if challenge.creator_id != current_user_id:

            return {
                "message":
                    "Only the challenge creator can assign winners."
            }, 403



        data = request.get_json()


        if not data:

            return {
                "message":
                    "Request body is required."
            }, 400



        submission_id = data.get(
            "submission_id"
        )


        if not submission_id:

            return {
                "message":
                    "submission_id is required."
            }, 400



        submission = ChallengeSubmission.query.get_or_404(
            submission_id
        )



        if submission.challenge_id != challenge_id:

            return {

                "message":
                    "Submission does not belong to this challenge."

            }, 400




        # Prevent duplicate reward

        existing_reward = ChallengeReward.query.filter_by(
            submission_id=submission.id
        ).first()


        if existing_reward:

            return {

                "message":
                    "This submission already has a reward."

            }, 400




        # Remove previous winner

        previous_winner = ChallengeSubmission.query.filter_by(

            challenge_id=challenge_id,

            is_winner=True

        ).first()



        if previous_winner:

            previous_winner.is_winner = False

            previous_winner.ranking = None




        # Set winner

        submission.is_winner = True

        submission.ranking = 1




        # Create reward

        reward = ChallengeReward(

            challenge_id=challenge_id,

            submission_id=submission.id,

            user_id=submission.user_id,


            reward_name=data.get(

                "reward_name",

                "BIG F Winner Prize"

            ),


            reward_description=data.get(

                "reward_description"

            ),


            reward_value=data.get(

                "reward_value"

            ),


            position=1,


            status="approved",


            rewarded_at=datetime.now(
                timezone.utc
            )

        )



        challenge.status = "completed"



        db.session.add(
            reward
        )


        db.session.commit()



        return {


            "message":
                "Winner selected successfully.",



            "winner":

            {

                "user_id":
                    submission.user_id,


                "username":
                    submission.user.username,


                "submission_id":
                    submission.id

            },


            "reward_id":
                reward.id


        }, 201







# ============================================================
# GET ONE REWARD
# ============================================================

class ChallengeRewardDetailResource(Resource):


    def get(self, reward_id):


        reward = ChallengeReward.query.get_or_404(
            reward_id
        )



        return {


            "id":
                reward.id,


            "challenge_id":
                reward.challenge_id,


            "submission_id":
                reward.submission_id,



            "winner":

            {

                "id":
                    reward.user.id,


                "username":
                    reward.user.username

            },



            "reward_name":
                reward.reward_name,



            "reward_description":
                reward.reward_description,



            "reward_value":

                float(reward.reward_value)

                if reward.reward_value

                else None,



            "position":
                reward.position,



            "status":
                reward.status,



            "rewarded_at":

                reward.rewarded_at.isoformat()

                if reward.rewarded_at

                else None


        }, 200





# ============================================================
# UPDATE REWARD STATUS
# ============================================================


    @jwt_required()
    def put(self, reward_id):


        current_user_id = int(
            get_jwt_identity()
        )



        reward = ChallengeReward.query.get_or_404(
            reward_id
        )



        if reward.challenge.creator_id != current_user_id:


            return {


                "message":
                    "Only challenge creator can update reward."

            }, 403




        data = request.get_json()



        if not data:

            return {

                "message":
                    "Request body required."

            }, 400




        if "status" in data:

            reward.status = data["status"]




        if "reward_description" in data:

            reward.reward_description = data[
                "reward_description"
            ]




        if reward.status == "delivered":

            reward.rewarded_at = datetime.now(
                timezone.utc
            )




        db.session.commit()



        return {


            "message":
                "Reward updated successfully."

        }, 200







# ============================================================
# USER REWARD HISTORY
# ============================================================

class UserRewardsResource(Resource):


    @jwt_required()
    def get(self):


        current_user_id = int(
            get_jwt_identity()
        )



        rewards = ChallengeReward.query.filter_by(

            user_id=current_user_id

        ).all()



        reward_list = []



        for reward in rewards:


            reward_list.append({


                "id":
                    reward.id,



                "challenge":

                {

                    "id":
                        reward.challenge.id,


                    "title":
                        reward.challenge.title

                },



                "reward_name":
                    reward.reward_name,



                "reward_value":

                    float(reward.reward_value)

                    if reward.reward_value

                    else None,



                "position":
                    reward.position,



                "status":
                    reward.status,



                "rewarded_at":

                    reward.rewarded_at.isoformat()

                    if reward.rewarded_at

                    else None


            })



        return reward_list, 200