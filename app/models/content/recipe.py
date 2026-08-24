from datetime import datetime, timezone

from app.extensions import db


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Creator of the recipe
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    instructions = db.Column(
        db.Text,
        nullable=False
    )

    thumbnail = db.Column(
        db.String(500),
        nullable=True
    )

    cooking_time = db.Column(
        db.Integer,
        nullable=True
    )

    servings = db.Column(
        db.Integer,
        nullable=True
    )

    difficulty = db.Column(
        db.String(20),
        default="Easy",
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="published",
        nullable=False
    )

    views = db.Column(
        db.Integer,
        default=0,
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

    # -------------------------
    # Relationships
    # -------------------------

    # Recipe creator
    user = db.relationship(
        "User",
        back_populates="recipes"
    )

    # Ingredients
    recipe_ingredients = db.relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    # Posts sharing this recipe
    posts = db.relationship(
        "Post",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    # Ratings
    ratings = db.relationship(
        "RecipeRating",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    # Saved recipes
    saved_by_users = db.relationship(
        "SavedRecipe",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    # Challenge submissions
    challenge_submissions = db.relationship(
        "ChallengeSubmission",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    # Shop products linked to this recipe
    product_links = db.relationship(
        "ProductRecipe",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Recipe {self.title}>"
