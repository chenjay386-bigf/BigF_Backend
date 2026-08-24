from datetime import datetime, timezone

from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    sku = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    stock_quantity = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    image_url = db.Column(
        db.String(500),
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
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

    # Category
    category = db.relationship(
        "Category",
        back_populates="products"
    )

    # Recipes using this product
    recipe_links = db.relationship(
        "ProductRecipe",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # Cart items containing this product
    cart_items = db.relationship(
        "CartItem",
        back_populates="product"
    )

    # Order items containing this product
    order_items = db.relationship(
        "OrderItem",
        back_populates="product"
    )
