from app.extensions import ma
from app.models.shop.cart import Cart


class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True
        include_fk = True
        ordered = True


cart_schema = CartSchema()
carts_schema = CartSchema(many=True)
