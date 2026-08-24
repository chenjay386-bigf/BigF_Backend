from datetime import datetime, timezone

from app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # User who created the post
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Optional recipe attached to the post
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        nullable=True,
        index=True
    )

    # Post caption
    caption = db.Column(
        db.Text,
        nullable=True
    )

    # Post status
    status = db.Column(
        db.String(20),
        default="published",
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

    # ==========================
    # Relationships
    # ==========================

    user = db.relationship(
        "User",
        back_populates="posts"
    )

    recipe = db.relationship(
        "Recipe",
        back_populates="posts"
    )

    media = db.relationship(
        "Media",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    comments = db.relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    likes = db.relationship(
        "Like",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    reshares = db.relationship(
        "Reshare",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    social_media_submissions = db.relationship(
        "SocialMediaSubmission",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    challenge_submissions = db.relationship(
        "ChallengeSubmission",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Post {self.id}>"
