from app.extensions import ma
from app.models.content.recipe_ingredient import RecipeIngredient


class RecipeIngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeIngredient
        load_instance = True
        include_fk = True
        ordered = True


recipe_ingredient_schema = RecipeIngredientSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)
