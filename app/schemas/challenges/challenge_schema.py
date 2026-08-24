from marshmallow import fields

from app.extensions import ma

from app.models.challenges.challenge import Challenge


class ChallengeSchema(ma.SQLAlchemyAutoSchema):

    creator_username = fields.String(
        attribute="creator.username",
        dump_only=True
    )

    submission_count = fields.Method(
        "get_submission_count"
    )

    has_reward = fields.Method(
        "get_has_reward"
    )

    class Meta:

        model = Challenge

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )

    def get_submission_count(self, obj):

        return len(obj.submissions)

    def get_has_reward(self, obj):

        return obj.reward is not None


challenge_schema = ChallengeSchema()

challenges_schema = ChallengeSchema(
    many=True
)