from marshmallow import fields

from app.extensions import ma

from app.models.content.like import Like


class LikeSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    class Meta:

        model = Like

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at"
        )


like_schema = LikeSchema()

likes_schema = LikeSchema(
    many=True
)