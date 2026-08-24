from datetime import datetime, timezone

from app.extensions import db


class ChallengeSubmission(db.Model):

    __tablename__ = "challenge_submissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================
    # CHALLENGE CONNECTION
    # ==========================================

    challenge_id = db.Column(
        db.Integer,
        db.ForeignKey("challenges.id"),
        nullable=False,
        index=True
    )

    # User who participated
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # ==========================================
    # COMMUNITY CONTENT
    # ==========================================

    # Optional recipe entry
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        nullable=True
    )

    # Optional video/photo post
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=True
    )

    # ==========================================
    # TIKTOK CHALLENGE ENTRY
    # ==========================================

    # TikTok video submitted for this challenge
    tiktok_url = db.Column(
        db.String(500),
        nullable=True
    )

    # ==========================================
    # MODERATION
    # ==========================================

    # pending  = waiting for admin review
    # approved = visible/eligible for voting
    # rejected = not eligible for voting
    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
        index=True
    )

    # Optional reason when admin rejects submission
    moderation_note = db.Column(
        db.Text,
        nullable=True
    )

    # Participant explanation
    description = db.Column(
        db.Text,
        nullable=True
    )

    # ==========================================
    # WINNER SYSTEM
    # ==========================================

    # False = participant
    # True = winner
    is_winner = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # Position in challenge
    # Example:
    # 1 = winner
    # 2 = runner up
    # 3 = third place
    ranking = db.Column(
        db.Integer,
        nullable=True
    )

    # ==========================================
    # TIMESTAMP
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

    challenge = db.relationship(
        "Challenge",
        back_populates="submissions"
    )

    user = db.relationship(
        "User",
        back_populates="challenge_submissions"
    )

    recipe = db.relationship(
        "Recipe",
        back_populates="challenge_submissions"
    )

    post = db.relationship(
        "Post",
        back_populates="challenge_submissions"
    )

    # Votes received
    votes = db.relationship(
        "ChallengeVote",
        back_populates="submission",
        cascade="all, delete-orphan"
    )

    # Reward if winner
    reward = db.relationship(
        "ChallengeReward",
        back_populates="submission",
        uselist=False
    )

    # ==========================================
    # HELPER METHODS
    # ==========================================

    def vote_count(self):
        return len(self.votes)

    def is_pending(self):
        return self.status == "pending"

    def is_approved(self):
        return self.status == "approved"

    def is_rejected(self):
        return self.status == "rejected"

    def __repr__(self):

        return (
            f"<ChallengeSubmission("
            f"id={self.id}, "
            f"user={self.user_id}, "
            f"challenge={self.challenge_id}, "
            f"status={self.status}, "
            f"winner={self.is_winner})>"
        )