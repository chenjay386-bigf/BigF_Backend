from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint

from app.extensions import db


class Reshare(db.Model):
    __tablename__ = "reshares"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # User who reshared the post
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Original post being reshared
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
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
        back_populates="reshares"
    )

    post = db.relationship(
        "Post",
        back_populates="reshares"
    )

    # ==========================================
    # Constraints
    # ==========================================

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="unique_user_post_reshare"
        ),
    )

    def __repr__(self):
        return (
            f"<Reshare(user={self.user_id}, "
            f"post={self.post_id})>"
        )
