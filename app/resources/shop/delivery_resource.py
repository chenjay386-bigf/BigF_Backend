from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request

from app.extensions import db
from app.models.shop.delivery import Delivery
from app.models.shop.order import Order


class DeliveryResource(Resource):
    """
    Create and list deliveries for authenticated users.
    """

    @jwt_required()
    def post(self):

        current_user_id = int(get_jwt_identity())

        data = request.get_json()

        order_id = data.get("order_id")
        recipient_name = data.get("recipient_name")
        recipient_phone = data.get("recipient_phone")
        county = data.get("county")
        town = data.get("town")
        address = data.get("address")


        if not order_id:
            return {
                "message": "Order ID is required."
            }, 400


        required_fields = [
            recipient_name,
            recipient_phone,
            county,
            town
        ]

        if not all(required_fields):
            return {
                "message": "Recipient name, phone, county and town are required."
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



        existing_delivery = Delivery.query.filter_by(
            order_id=order_id
        ).first()


        if existing_delivery:
            return {
                "message": "Delivery already exists for this order."
            }, 400



        delivery = Delivery(
            order_id=order.id,
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            county=county,
            town=town,
            address=address,
            status="pending"
        )


        db.session.add(delivery)
        db.session.commit()



        return {
            "message": "Delivery created successfully.",
            "delivery_id": delivery.id,
            "status": delivery.status
        }, 201





    @jwt_required()
    def get(self):

        current_user_id = int(get_jwt_identity())


        deliveries = (
            Delivery.query
            .join(Order)
            .filter(Order.user_id == current_user_id)
            .all()
        )


        delivery_list = []


        for delivery in deliveries:

            delivery_list.append({

                "id": delivery.id,

                "order_id": delivery.order_id,

                "recipient_name":
                    delivery.recipient_name,

                "recipient_phone":
                    delivery.recipient_phone,

                "county":
                    delivery.county,

                "town":
                    delivery.town,

                "address":
                    delivery.address,

                "status":
                    delivery.status,

                "created_at":
                    delivery.created_at.isoformat()
                    if delivery.created_at
                    else None,

                "updated_at":
                    delivery.updated_at.isoformat()
                    if delivery.updated_at
                    else None
            })


        return delivery_list, 200





class DeliveryDetailResource(Resource):
    """
    Get delivery details for a specific delivery.
    """


    @jwt_required()
    def get(self, delivery_id):

        current_user_id = int(get_jwt_identity())


        delivery = Delivery.query.get_or_404(
            delivery_id
        )


        if delivery.order.user_id != current_user_id:
            return {
                "message": "Unauthorized access."
            }, 403



        return {

            "id": delivery.id,

            "order_id":
                delivery.order_id,

            "recipient_name":
                delivery.recipient_name,

            "recipient_phone":
                delivery.recipient_phone,

            "county":
                delivery.county,

            "town":
                delivery.town,

            "address":
                delivery.address,

            "status":
                delivery.status,

            "created_at":
                delivery.created_at.isoformat()
                if delivery.created_at
                else None,

            "updated_at":
                delivery.updated_at.isoformat()
                if delivery.updated_at
                else None

        }, 200