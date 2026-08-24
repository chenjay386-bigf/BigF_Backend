from marshmallow import fields

from app.extensions import ma
from app.models.content.recipe import Recipe


class RecipeSchema(ma.SQLAlchemyAutoSchema):

    creator = fields.String(
        attribute="user.username",
        dump_only=True
    )

    average_rating = fields.Method(
        "get_average_rating"
    )

    rating_count = fields.Method(
        "get_rating_count"
    )

    saved_count = fields.Method(
        "get_saved_count"
    )

    post_count = fields.Method(
        "get_post_count"
    )

    ingredient_count = fields.Method(
        "get_ingredient_count"
    )

    class Meta:

        model = Recipe

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )

    def get_average_rating(self, obj):

        if not obj.ratings:
            return 0

        total = sum(
            rating.rating
            for rating in obj.ratings
        )

        return round(
            total / len(obj.ratings),
            1
        )

    def get_rating_count(self, obj):

        return len(
            obj.ratings
        )

    def get_saved_count(self, obj):

        return len(
            obj.saved_by_users
        )

    def get_post_count(self, obj):

        return len(
            obj.posts
        )

    def get_ingredient_count(self, obj):

        return len(
            obj.recipe_ingredients
        )


recipe_schema = RecipeSchema()

recipes_schema = RecipeSchema(
    many=True
)