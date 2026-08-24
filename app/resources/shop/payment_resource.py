from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request

from app.extensions import db
from app.models.shop.payment import Payment
from app.models.shop.order import Order


class PaymentResource(Resource):
    """
    Create and list payments.
    """

    @jwt_required()
    def post(self):

        current_user_id = get_jwt_identity()

        data = request.get_json()

        order_id = data.get("order_id")
        payment_method = data.get("payment_method")
        transaction_id = data.get("transaction_id")

        if not order_id:
            return {
                "message": "Order ID is required."
            }, 400

        order = Order.query.get(order_id)

        if not order:
            return {
                "message": "Order not found."
            }, 404

        # Security check
        if order.user_id != current_user_id:
            return {
                "message": "Unauthorized access."
            }, 403


        payment = Payment(
            order_id=order.id,
            amount=float(order.total_amount),
            payment_method=payment_method,
            status="pending",
            transaction_reference=transaction_id
        )


        db.session.add(payment)
        db.session.commit()


        return {
            "message": "Payment created successfully.",
            "payment_id": payment.id,
            "amount": float(payment.amount),
            "status": payment.status
        }, 201



    @jwt_required()
    def get(self):

        current_user_id = get_jwt_identity()


        payments = (
            Payment.query
            .join(Order)
            .filter(Order.user_id == current_user_id)
            .all()
        )


        payment_list = []


        for payment in payments:

            payment_list.append({

                "id": payment.id,
                "order_id": payment.order_id,
                "amount": float(payment.amount),
                "payment_method": payment.payment_method,
                "status": payment.status,
                "transaction_reference": payment.transaction_reference,

                "created_at":
                    payment.created_at.isoformat()
                    if payment.created_at
                    else None

            })


        return payment_list, 200



class PaymentDetailResource(Resource):
    """
    Get a single payment.
    """

    @jwt_required()
    def get(self, payment_id):

        current_user_id = get_jwt_identity()


        payment = Payment.query.get_or_404(payment_id)


        if payment.order.user_id != current_user_id:
            return {
                "message": "Unauthorized access."
            },403



        return {

            "id": payment.id,

            "order_id": payment.order_id,

            "amount": float(payment.amount),

            "payment_method":
                payment.payment_method,

            "status":
                payment.status,

            "transaction_reference":
                payment.transaction_reference,

            "created_at":
                payment.created_at.isoformat()
                if payment.created_at
                else None

        },200