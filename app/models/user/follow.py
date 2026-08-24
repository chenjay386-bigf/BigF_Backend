from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, UniqueConstraint

from app.extensions import db


class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    follower_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    following_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # User who is following
    follower = db.relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following"
    )

    # User being followed
    following = db.relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followers"
    )

    __table_args__ = (
        UniqueConstraint(
            "follower_id",
            "following_id",
            name="unique_user_follow"
        ),

        CheckConstraint(
            "follower_id != following_id",
            name="prevent_self_follow"
        ),
    )

    def __repr__(self):
        return f"<Follow {self.follower_id} -> {self.following_id}>"
