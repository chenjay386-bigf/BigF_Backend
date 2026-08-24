from app.extensions import db

from sqlalchemy import UniqueConstraint


class ProductRecipe(db.Model):
    __tablename__ = "product_recipes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        nullable=False
    )

    product = db.relationship(
        "Product",
        back_populates="recipe_links"
    )

    recipe = db.relationship(
        "Recipe",
        back_populates="product_links"
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "recipe_id",
            name="unique_product_recipe"
        ),
    )
