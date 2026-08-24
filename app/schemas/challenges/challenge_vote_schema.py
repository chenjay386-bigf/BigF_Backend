from marshmallow import fields

from app.extensions import ma

from app.models.challenges.challenge_vote import ChallengeVote


class ChallengeVoteSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    class Meta:

        model = ChallengeVote

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at"
        )


challenge_vote_schema = ChallengeVoteSchema()

challenge_votes_schema = ChallengeVoteSchema(
    many=True
)