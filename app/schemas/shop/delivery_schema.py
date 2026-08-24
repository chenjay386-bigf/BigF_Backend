from app.extensions import ma
from app.models.shop.delivery import Delivery


class DeliverySchema(ma.SQLAlchemyAutoSchema):

    class Meta:

        model = Delivery

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )


delivery_schema = DeliverySchema()

deliveries_schema = DeliverySchema(
    many=True
)