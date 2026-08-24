from marshmallow import fields

from app.extensions import ma

from app.models.challenges.challenge_reward import (
    ChallengeReward
)


class ChallengeRewardSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    challenge_title = fields.String(
        attribute="challenge.title",
        dump_only=True
    )

    class Meta:

        model = ChallengeReward

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )


challenge_reward_schema = (
    ChallengeRewardSchema()
)

challenge_rewards_schema = (
    ChallengeRewardSchema(
        many=True
    )
)