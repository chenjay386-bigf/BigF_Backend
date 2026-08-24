from marshmallow import fields

from app.extensions import ma
from app.models.content.saved_recipe import SavedRecipe


class SavedRecipeSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    recipe_title = fields.String(
        attribute="recipe.title",
        dump_only=True
    )

    class Meta:

        model = SavedRecipe

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at"
        )


saved_recipe_schema = SavedRecipeSchema()

saved_recipes_schema = SavedRecipeSchema(
    many=True
)