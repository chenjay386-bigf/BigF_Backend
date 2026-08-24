from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint

from app.extensions import db


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # User who liked the post
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Post being liked
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

    # ==========================
    # Relationships
    # ==========================

    user = db.relationship(
        "User",
        back_populates="likes"
    )

    post = db.relationship(
        "Post",
        back_populates="likes"
    )

    # ==========================
    # Constraints
    # ==========================

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="unique_user_post_like"
        ),
    )

    def __repr__(self):
        return (
            f"<Like(user={self.user_id}, "
            f"post={self.post_id})>"
        )
