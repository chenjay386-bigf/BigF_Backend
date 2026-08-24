
from datetime import datetime, timezone

from app.extensions import db


class ChallengeReward(db.Model):

    __tablename__ = "challenge_rewards"


    # ============================================================
    # PRIMARY KEY
    # ============================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # ============================================================
    # CONNECTIONS
    # ============================================================


    # Challenge that was won
    challenge_id = db.Column(
        db.Integer,
        db.ForeignKey("challenges.id"),
        nullable=False,
        index=True
    )


    # Winning submission
    submission_id = db.Column(
        db.Integer,
        db.ForeignKey("challenge_submissions.id"),
        nullable=False,
        unique=True,
        index=True
    )


    # Winner
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )



    # ============================================================
    # REWARD INFORMATION
    # ============================================================


    reward_name = db.Column(
        db.String(255),
        nullable=False
    )


    reward_description = db.Column(
        db.Text,
        nullable=True
    )


    # Optional cash value
    reward_value = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )


    # Winner position
    # 1 = Winner
    # 2 = Runner up
    # 3 = Third place

    position = db.Column(
        db.Integer,
        nullable=True
    )


    # pending
    # approved
    # delivered
    # cancelled

    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )


    rewarded_at = db.Column(
        db.DateTime,
        nullable=True
    )



    # ============================================================
    # TIMESTAMPS
    # ============================================================


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



    # ============================================================
    # RELATIONSHIPS
    # ============================================================


    challenge = db.relationship(
        "Challenge",
        back_populates="reward"
    )


    submission = db.relationship(
        "ChallengeSubmission",
        back_populates="reward"
    )


    user = db.relationship(
        "User",
        back_populates="challenge_rewards"
    )



    # ============================================================
    # METHODS
    # ============================================================


    def mark_delivered(self):

        self.status = "delivered"

        self.rewarded_at = datetime.now(
            timezone.utc
        )



    def __repr__(self):

        return (
            f"<ChallengeReward("
            f"id={self.id}, "
            f"challenge={self.challenge_id}, "
            f"user={self.user_id}, "
            f"position={self.position}, "
            f"status='{self.status}')>"
        )