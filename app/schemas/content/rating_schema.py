from marshmallow import fields

from app.extensions import ma

from app.models.content.recipe_rating import RecipeRating


class RecipeRatingSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    class Meta:

        model = RecipeRating

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )


recipe_rating_schema = RecipeRatingSchema()

recipe_ratings_schema = RecipeRatingSchema(
    many=True
)