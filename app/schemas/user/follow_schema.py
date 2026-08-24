from marshmallow import fields

from app.extensions import ma

from app.models.user.follow import Follow


class FollowSchema(ma.SQLAlchemyAutoSchema):

    follower_username = fields.String(
        attribute="follower.username",
        dump_only=True
    )

    following_username = fields.String(
        attribute="following.username",
        dump_only=True
    )

    class Meta:

        model = Follow

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
        )


follow_schema = FollowSchema()

follows_schema = FollowSchema(
    many=True
)