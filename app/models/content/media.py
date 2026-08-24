from datetime import datetime, timezone

from app.extensions import db


class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Post this media belongs to
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False,
        index=True
    )

    # Cloudinary URL
    url = db.Column(
        db.String(500),
        nullable=False
    )

    # image or video
    media_type = db.Column(
        db.String(20),
        nullable=False
    )

    # Cloudinary Public ID
    public_id = db.Column(
        db.String(255),
        nullable=False
    )

    # Display order
    position = db.Column(
        db.Integer,
        default=1,
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

    post = db.relationship(
        "Post",
        back_populates="media"
    )

    def __repr__(self):
        return f"<Media {self.id} ({self.media_type})>"
