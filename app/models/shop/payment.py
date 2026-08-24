from datetime import datetime, timezone

from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    # Amount for this payment
    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    # mpesa, card, cash, etc.
    payment_method = db.Column(
        db.String(50),
        nullable=False
    )

    # pending, completed, failed, refunded
    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    # M-Pesa transaction code or payment reference
    transaction_reference = db.Column(
        db.String(255),
        unique=True,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    order = db.relationship(
        "Order",
        back_populates="payments"
    )
