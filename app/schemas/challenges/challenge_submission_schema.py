from marshmallow import fields

from app.extensions import ma

from app.models.challenges.challenge_submission import (
    ChallengeSubmission
)


class ChallengeSubmissionSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    challenge_title = fields.String(
        attribute="challenge.title",
        dump_only=True
    )

    recipe_title = fields.String(
        attribute="recipe.title",
        dump_only=True,
        allow_none=True
    )

    vote_count = fields.Method(
        "get_vote_count"
    )

    class Meta:

        model = ChallengeSubmission

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )

    def get_vote_count(self, obj):

        return len(obj.votes)


challenge_submission_schema = (
    ChallengeSubmissionSchema()
)

challenge_submissions_schema = (
    ChallengeSubmissionSchema(
        many=True
    )
)