from datetime import datetime, timezone

from app.extensions import db


class SocialMediaSubmission(db.Model):
    __tablename__ = "social_media_submissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # User who submitted the link
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Optional BIG F post associated with the submission
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=True,
        index=True
    )

    # Platform (TikTok, Instagram, Facebook, YouTube, X, etc.)
    platform = db.Column(
        db.String(50),
        nullable=False
    )

    # URL to the social media post
    url = db.Column(
        db.String(500),
        nullable=False
    )

    # Submission status
    status = db.Column(
        db.String(20),
        default="pending",
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
        back_populates="social_media_submissions"
    )

    post = db.relationship(
        "Post",
        back_populates="social_media_submissions"
    )

    def __repr__(self):
        return (
            f"<SocialMediaSubmission("
            f"user={self.user_id}, "
            f"platform='{self.platform}')>"
        )
