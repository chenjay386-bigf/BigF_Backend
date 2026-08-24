from marshmallow import fields

from app.extensions import ma
from app.models.content.post import Post


class PostSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    recipe_title = fields.String(
        attribute="recipe.title",
        dump_only=True,
        allow_none=True
    )

    media_count = fields.Method(
        "get_media_count"
    )

    comment_count = fields.Method(
        "get_comment_count"
    )

    like_count = fields.Method(
        "get_like_count"
    )

    reshare_count = fields.Method(
        "get_reshare_count"
    )

    class Meta:

        model = Post

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )

    def get_media_count(self, obj):

        return len(obj.media)

    def get_comment_count(self, obj):

        return len(obj.comments)

    def get_like_count(self, obj):

        return len(obj.likes)

    def get_reshare_count(self, obj):

        return len(obj.reshares)


post_schema = PostSchema()

posts_schema = PostSchema(
    many=True
)