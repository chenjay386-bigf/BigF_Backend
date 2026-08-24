from marshmallow import fields

from app.extensions import ma
from app.models.shop.order import Order


class OrderSchema(ma.SQLAlchemyAutoSchema):

    item_count = fields.Method(
        "get_item_count"
    )

    class Meta:

        model = Order

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )

    def get_item_count(self, obj):

        return len(obj.order_items)


order_schema = OrderSchema()

orders_schema = OrderSchema(
    many=True
)