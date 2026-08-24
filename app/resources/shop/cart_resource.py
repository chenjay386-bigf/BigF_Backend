from flask import request
from flask_restful import Resource

from app.extensions import db

from app.models.shop.cart import Cart
from app.models.user.user import User



# ============================================================
# CART RESOURCE
# ============================================================

class CartResource(Resource):


    # GET USER CART

    def get(self, user_id):

        cart = Cart.query.filter_by(
            user_id=user_id
        ).first()


        if not cart:

            return {

                "message":
                    "Cart not found."

            }, 404



        return {


            "id":
                cart.id,


            "user_id":
                cart.user_id,


            "items":

            [

                {

                    "id":
                        item.id,


                    "product_id":
                        item.product_id,


                    "quantity":
                        item.quantity

                }

                for item in cart.items

            ]

        }, 200





    # CREATE CART

    def post(self, user_id):


        user = User.query.get(user_id)


        if not user:

            return {

                "message":
                    "User not found."

            },404



        existing = Cart.query.filter_by(
            user_id=user_id
        ).first()



        if existing:

            return {

                "message":
                    "User already has a cart.",

                "cart_id":
                    existing.id

            },400



        cart = Cart(

            user_id=user_id

        )


        db.session.add(cart)

        db.session.commit()



        return {


            "message":
                "Cart created successfully.",


            "cart_id":
                cart.id


        },201