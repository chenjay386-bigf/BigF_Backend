from datetime import datetime, timezone

from app.extensions import db


class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    # Customer's delivery details
    recipient_name = db.Column(
        db.String(255),
        nullable=False
    )

    recipient_phone = db.Column(
        db.String(50),
        nullable=False
    )

    county = db.Column(
        db.String(100),
        nullable=False
    )

    town = db.Column(
        db.String(100),
        nullable=False
    )

    address = db.Column(
        db.String(500),
        nullable=True
    )

    # pending, processing, shipped,
    # out_for_delivery, delivered
    status = db.Column(
        db.String(30),
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

    order = db.relationship(
        "Order",
        back_populates="delivery"
    )
