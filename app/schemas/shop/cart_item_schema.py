from marshmallow import fields

from app.extensions import ma
from app.models.shop.cart_item import CartItem


class CartItemSchema(ma.SQLAlchemyAutoSchema):

    product_name = fields.String(
        attribute="product.name",
        dump_only=True
    )

    subtotal = fields.Method(
        "get_subtotal"
    )

    class Meta:

        model = CartItem

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )

    def get_subtotal(self, obj):

        return float(
            obj.quantity * obj.product.price
        )


cart_item_schema = CartItemSchema()

cart_items_schema = CartItemSchema(
    many=True
)