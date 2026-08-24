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
# CHALLENGE RESOURCE
# GET ALL CHALLENGES
# CREATE CHALLENGE
# ============================================================

class ChallengeResource(Resource):


    def get(self):

        challenges = Challenge.query.order_by(
            Challenge.created_at.desc()
        ).all()


        challenge_list = []


        for challenge in challenges:

            challenge_list.append({

                "id": challenge.id,

                "title": challenge.title,

                "description": challenge.description,

                "rules": challenge.rules,

                "category": challenge.category,

                "banner_image": challenge.banner_image,

                "creator_id": challenge.creator_id,

                "status": challenge.status,


                "start_date":
                    challenge.start_date.isoformat(),


                "end_date":
                    challenge.end_date.isoformat(),


                "participants":
                    challenge.submissions.count(),


                "created_at":
                    challenge.created_at.isoformat()

            })


        return challenge_list, 200



    # ========================================================
    # CREATE CHALLENGE
    # ========================================================

    @jwt_required()
    def post(self):

        current_user_id = int(
            get_jwt_identity()
        )


        data = request.get_json()


        if not data:

            return {

                "message":
                "Request body is required."

            }, 400



        required_fields = [
            "title",
            "start_date",
            "end_date"
        ]


        for field in required_fields:

            if not data.get(field):

                return {

                    "message":
                    f"{field} is required."

                }, 400




        challenge = Challenge(

            title=data.get("title"),

            description=data.get("description"),

            rules=data.get("rules"),

            category=data.get("category"),

            banner_image=data.get("banner_image"),

            creator_id=current_user_id,

            start_date=data.get("start_date"),

            end_date=data.get("end_date"),

            status=data.get(
                "status",
                "draft"
            )

        )



        db.session.add(
            challenge
        )


        db.session.commit()



        return {


            "message":
            "Challenge created successfully.",


            "challenge_id":
            challenge.id


        }, 201





# ============================================================
# CHALLENGE DETAIL RESOURCE
# ============================================================

class ChallengeDetailResource(Resource):


    def get(self, challenge_id):

        challenge = Challenge.query.get_or_404(
            challenge_id
        )



        return {


            "id":
            challenge.id,


            "title":
            challenge.title,


            "description":
            challenge.description,


            "rules":
            challenge.rules,


            "category":
            challenge.category,


            "banner_image":
            challenge.banner_image,


            "creator_id":
            challenge.creator_id,


            "status":
            challenge.status,


            "start_date":
            challenge.start_date.isoformat(),


            "end_date":
            challenge.end_date.isoformat(),


            "participants":
            challenge.submissions.count(),


            "created_at":
            challenge.created_at.isoformat()


        }, 200





    # ========================================================
    # DELETE CHALLENGE
    # ========================================================


    @jwt_required()
    def delete(self, challenge_id):


        current_user_id = int(
            get_jwt_identity()
        )



        challenge = Challenge.query.get_or_404(
            challenge_id
        )



        if challenge.creator_id != current_user_id:


            return {


                "message":
                "Only the challenge creator can delete this challenge."


            }, 403




        db.session.delete(
            challenge
        )


        db.session.commit()



        return {


            "message":
            "Challenge deleted successfully."


        }, 200






# ============================================================
# CHALLENGE PARTICIPANTS
# ============================================================


class ChallengeParticipantsResource(Resource):


    def get(self, challenge_id):


        challenge = Challenge.query.get_or_404(
            challenge_id
        )



        submissions = ChallengeSubmission.query.filter_by(
            challenge_id=challenge.id
        ).all()



        participants = []



        for submission in submissions:


            participants.append({


                "submission_id":
                submission.id,


                "user": {


                    "id":
                    submission.user.id,


                    "username":
                    submission.user.username


                },


                "recipe_id":
                submission.recipe_id,


                "post_id":
                submission.post_id,


                "description":
                submission.description,


                "submitted_at":
                submission.created_at.isoformat()


            })




        return {


            "challenge_id":
            challenge.id,


            "challenge_title":
            challenge.title,


            "total_participants":
            len(participants),


            "participants":
            participants


        }, 200






# ============================================================
# CHALLENGE WINNER
# ============================================================


class ChallengeWinnerResource(Resource):


    def get(self, challenge_id):


        challenge = Challenge.query.get_or_404(
            challenge_id
        )



        reward = ChallengeReward.query.filter_by(
            challenge_id=challenge.id
        ).first()



        if not reward:


            return {


                "message":
                "Winner has not been announced yet."


            }, 404




        submission = reward.submission




        return {


            "challenge_id":
            challenge.id,


            "challenge":
            challenge.title,



            "winner": {


                "user_id":
                submission.user.id,


                "username":
                submission.user.username,


                "submission_id":
                submission.id,


                "reward":
                reward.reward_name,


                "reward_description":
                reward.reward_description


            }


        }, 200