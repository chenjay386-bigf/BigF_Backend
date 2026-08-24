

from flask import request 
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.shop.cart import Cart
from app.models.shop.cart_item import CartItem
from app.models.shop.product import Product



# ============================================================
# CART ITEMS LIST / CREATE
# ============================================================

class CartItemResource(Resource):

    @jwt_required()
    def get(self, cart_id):

        cart = Cart.query.get_or_404(cart_id)

        items = []

        for item in cart.items:

            items.append({
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": float(item.product.price),
                "subtotal": float(item.product.price * item.quantity)
            })


        return {
            "cart_id": cart.id,
            "items": items
        }, 200



    @jwt_required()
    def post(self, cart_id):

        data = request.get_json()

        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)


        product = Product.query.get_or_404(product_id)

        item = CartItem(
            cart_id=cart_id,
            product_id=product.id,
            quantity=quantity
        )


        db.session.add(item)
        db.session.commit()


        return {
            "message": "Product added to cart",
            "item_id": item.id
        }, 201





# ============================================================
# SINGLE CART ITEM
# ============================================================

class CartItemDetailResource(Resource):

    @jwt_required()
    def put(self, item_id):

        item = CartItem.query.get_or_404(item_id)

        data = request.get_json()

        item.quantity = data.get(
            "quantity",
            item.quantity
        )


        db.session.commit()


        return {
            "message": "Cart item updated"
        }, 200



    @jwt_required()
    def delete(self, item_id):

        item = CartItem.query.get_or_404(item_id)


        db.session.delete(item)
        db.session.commit()


        return {
            "message": "Cart item removed"
        }, 200