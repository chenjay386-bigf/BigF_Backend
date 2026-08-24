from datetime import datetime, timezone

from app.extensions import db



class ChallengeVote(db.Model):

    __tablename__ = "challenge_votes"


    # ============================================================
    # PRIMARY KEY
    # ============================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )



    # ============================================================
    # CONNECTION TO SUBMISSION
    # ============================================================

    submission_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "challenge_submissions.id"
        ),
        nullable=False,
        index=True
    )



    # ============================================================
    # USER WHO VOTED
    # ============================================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id"
        ),
        nullable=False,
        index=True
    )



    # ============================================================
    # TIMESTAMP
    # ============================================================

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )



    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    submission = db.relationship(
        "ChallengeSubmission",
        back_populates="votes"
    )


    user = db.relationship(
        "User",
        back_populates="challenge_votes"
    )



    # ============================================================
    # REPRESENTATION
    # ============================================================

    def __repr__(self):

        return (
            f"<ChallengeVote "
            f"id={self.id} "
            f"user={self.user_id} "
            f"submission={self.submission_id}>"
        )