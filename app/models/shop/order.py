from datetime import datetime, timezone

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # pending, confirmed, processing,
    # shipped, delivered, cancelled
    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    # Total amount of the order
    total_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    # Amount already paid
    amount_paid = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    # Remaining balance
    balance = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
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

    # User who placed the order
    user = db.relationship(
        "User",
        back_populates="orders"
    )

    # Items in the order
    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    # Payment records
    payments = db.relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    # Delivery information
    delivery = db.relationship(
        "Delivery",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )
