from marshmallow import fields

from app.extensions import ma

from app.models.user.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):

    display_name = fields.String(
        attribute="profile.display_name",
        dump_only=True
    )

    profile_image = fields.String(
        attribute="profile.profile_image",
        dump_only=True
    )

    follower_count = fields.Method(
        "get_follower_count"
    )

    following_count = fields.Method(
        "get_following_count"
    )

    recipe_count = fields.Method(
        "get_recipe_count"
    )

    post_count = fields.Method(
        "get_post_count"
    )

    achievement_count = fields.Method(
        "get_achievement_count"
    )

    class Meta:

        model = User

        load_instance = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "last_login"
        )

        exclude = (
            "password_hash",
        )

    def get_follower_count(self, obj):

        return len(obj.followers)

    def get_following_count(self, obj):

        return len(obj.following)

    def get_recipe_count(self, obj):

        return len(obj.recipes)

    def get_post_count(self, obj):

        return len(obj.posts)

    def get_achievement_count(self, obj):

        return len(obj.challenge_rewards)


user_schema = UserSchema()

users_schema = UserSchema(
    many=True
)