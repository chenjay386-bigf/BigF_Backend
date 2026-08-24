from marshmallow import fields

from app.extensions import ma

from app.models.content.social_media_submission import (
    SocialMediaSubmission
)


class SocialMediaSubmissionSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    class Meta:

        model = SocialMediaSubmission

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )


social_media_submission_schema = SocialMediaSubmissionSchema()

social_media_submissions_schema = (
    SocialMediaSubmissionSchema(
        many=True
    )
)