from marshmallow import fields

from app.extensions import ma

from app.models.content.comment import Comment


class CommentSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    class Meta:

        model = Comment

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )


comment_schema = CommentSchema()

comments_schema = CommentSchema(
    many=True
)