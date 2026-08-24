from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, UniqueConstraint

from app.extensions import db


class RecipeRating(db.Model):
    __tablename__ = "recipe_ratings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # User who rated the recipe
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Recipe being rated
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        nullable=False,
        index=True
    )

    # Rating (1–5)
    rating = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # ==========================================
    # Relationships
    # ==========================================

    user = db.relationship(
        "User",
        back_populates="recipe_ratings"
    )

    recipe = db.relationship(
        "Recipe",
        back_populates="ratings"
    )

    # ==========================================
    # Constraints
    # ==========================================

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "recipe_id",
            name="unique_user_recipe_rating"
        ),
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="valid_recipe_rating"
        ),
    )

    def __repr__(self):
        return (
            f"<RecipeRating(user={self.user_id}, "
            f"recipe={self.recipe_id}, "
            f"rating={self.rating})>"
        )
