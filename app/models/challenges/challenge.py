from datetime import datetime, timezone

from app.extensions import db


class Challenge(db.Model):

    __tablename__ = "challenges"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # ==========================================
    # BASIC INFORMATION
    # ==========================================

    title = db.Column(
        db.String(255),
        nullable=False
    )


    description = db.Column(
        db.Text,
        nullable=True
    )


    # Challenge instructions
    # Example:
    # "Create a BIG F chicken noodle recipe video"
    rules = db.Column(
        db.Text,
        nullable=True
    )


    # Challenge type
    # Examples:
    # recipe
    # family
    # creative
    # video
    category = db.Column(
        db.String(50),
        nullable=True
    )


    banner_image = db.Column(
        db.String(500),
        nullable=True
    )


    # ==========================================
    # CREATOR
    # ==========================================

    # Usually admin account
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )


    # ==========================================
    # CAMPAIGN PERIOD
    # ==========================================

    start_date = db.Column(
        db.DateTime,
        nullable=False
    )


    end_date = db.Column(
        db.DateTime,
        nullable=False
    )


    # draft
    # active
    # completed
    # cancelled
    status = db.Column(
        db.String(20),
        default="draft",
        nullable=False
    )


    # ==========================================
    # TIMESTAMPS
    # ==========================================

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
    # RELATIONSHIPS
    # ==========================================


    # User who created challenge
    creator = db.relationship(
        "User",
        back_populates="created_challenges"
    )


    # All user entries
    submissions = db.relationship(
        "ChallengeSubmission",
        back_populates="challenge",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )


    # Winning reward
    reward = db.relationship(
        "ChallengeReward",
        back_populates="challenge",
        uselist=False,
        cascade="all, delete-orphan"
    )



    # ==========================================
    # HELPER METHODS
    # ==========================================


    def participant_count(self):

        return self.submissions.count()



    def winner(self):

        return self.submissions.filter_by(
            is_winner=True
        ).first()



    def __repr__(self):

        return (
            f"<Challenge("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status}')>"
        )