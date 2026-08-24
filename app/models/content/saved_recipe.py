from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint

from app.extensions import db


class SavedRecipe(db.Model):
    __tablename__ = "saved_recipes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # User who saved the recipe
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Recipe that was saved
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # ==========================================
    # Relationships
    # ==========================================

    user = db.relationship(
        "User",
        back_populates="saved_recipes"
    )

    recipe = db.relationship(
        "Recipe",
        back_populates="saved_by_users"
    )

    # ==========================================
    # Constraints
    # ==========================================

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "recipe_id",
            name="unique_user_saved_recipe"
        ),
    )

    def __repr__(self):
        return (
            f"<SavedRecipe(user={self.user_id}, "
            f"recipe={self.recipe_id})>"
        )
