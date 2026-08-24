from datetime import datetime, timezone

from app.extensions import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    display_name = db.Column(
        db.String(100),
        nullable=False
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    profile_image = db.Column(
        db.String(500),
        nullable=True
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

    # Relationship back to User
    user = db.relationship(
        "User",
        back_populates="profile"
    )

    def __repr__(self):
        return f"<Profile {self.display_name}>"
