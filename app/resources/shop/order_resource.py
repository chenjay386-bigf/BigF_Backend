from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.extensions import db
from app.models.shop.cart import Cart
from app.models.shop.order import Order


class OrderResource(Resource):
    """Create and list orders for the authenticated user."""

    @jwt_required()
    def post(self):

        current_user_id = int(get_jwt_identity())

        cart = Cart.query.filter_by(
            user_id=current_user_id
        ).first()

        if not cart or not cart.items:
            return {
                "message": "Your cart is empty."
            }, 400


        total_amount = 0.0


        for item in cart.items:

            total_amount += (
                float(item.product.price)
                * item.quantity
            )


        order = Order(
            user_id=current_user_id,
            total_amount=total_amount,
            status="pending"
        )


        db.session.add(order)
        db.session.commit()


        return {
            "message": "Order created successfully.",
            "order_id": order.id,
            "total_amount": total_amount
        }, 201





    @jwt_required()
    def get(self):

        current_user_id = int(get_jwt_identity())


        orders = Order.query.filter_by(
            user_id=current_user_id
        ).all()



        order_list = []


        for order in orders:

            order_list.append({

                "id": order.id,

                "status": order.status,

                "total_amount":
                    float(order.total_amount),

                "created_at":
                    (
                        order.created_at.isoformat()
                        if order.created_at
                        else None
                    ),

                "updated_at":
                    (
                        order.updated_at.isoformat()
                        if order.updated_at
                        else None
                    )

            })


        return order_list, 200







class OrderDetailResource(Resource):
    """Get a single order."""

    @jwt_required()
    def get(self, order_id):

        current_user_id = int(get_jwt_identity())


        order = Order.query.get_or_404(
            order_id
        )


        if order.user_id != current_user_id:

            return {
                "message": "Unauthorized access."
            }, 403




        return {

            "id": order.id,

            "status": order.status,


            "total_amount":
                float(order.total_amount),



            "created_at":
                (
                    order.created_at.isoformat()
                    if order.created_at
                    else None
                ),



            "updated_at":
                (
                    order.updated_at.isoformat()
                    if order.updated_at
                    else None
                ),




            "payments": [

                {
                    "id": payment.id,

                    "status": payment.status,

                    "method": payment.payment_method,

                    "amount": float(payment.amount),

                    "transaction_reference":
                        payment.transaction_reference
                }

                for payment in order.payments

            ],




            "delivery":
                (
                    {
                        "id": order.delivery.id,

                        "status": order.delivery.status,

                        "recipient_name":
                            order.delivery.recipient_name,

                        "recipient_phone":
                            order.delivery.recipient_phone,

                        "county":
                            order.delivery.county,

                        "town":
                            order.delivery.town,

                        "address":
                            order.delivery.address
                    }

                    if order.delivery

                    else None
                )

        }, 200