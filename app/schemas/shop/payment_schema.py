from app.extensions import ma
from app.models.shop.payment import Payment


class PaymentSchema(ma.SQLAlchemyAutoSchema):

    class Meta:

        model = Payment

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )


payment_schema = PaymentSchema()

payments_schema = PaymentSchema(
    many=True
)