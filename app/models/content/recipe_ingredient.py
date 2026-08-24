
from app.extensions import db


class RecipeIngredient(db.Model):

    __tablename__ = "recipe_ingredients"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "recipes.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredients.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    quantity = db.Column(
        db.String(100),
        nullable=True
    )

    unit = db.Column(
        db.String(50),
        nullable=True
    )

    # Relationships
    recipe = db.relationship(
        "Recipe",
        back_populates="recipe_ingredients"
    )

    ingredient = db.relationship(
        "Ingredient",
        back_populates="recipe_ingredients"
    )

    def __repr__(self):
        return (
            f"<RecipeIngredient "
            f"recipe_id={self.recipe_id} "
            f"ingredient_id={self.ingredient_id}>"
        )
