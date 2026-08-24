from flask import request
from flask_restful import Resource

from app.extensions import db

from app.models.shop.product import Product
from app.models.shop.category import Category



# ============================================================
# PRODUCTS LIST / CREATE
# ============================================================

class ProductResource(Resource):


    # GET ALL PRODUCTS
    def get(self):

        products = Product.query.all()


        return [

            {

                "id":
                    product.id,


                "category_id":
                    product.category_id,


                "name":
                    product.name,


                "description":
                    product.description,


                "sku":
                    product.sku,


                "price":
                    float(product.price),


                "stock_quantity":
                    product.stock_quantity,


                "image_url":
                    product.image_url,


                "is_active":
                    product.is_active

            }

            for product in products

        ], 200





    # CREATE PRODUCT
    def post(self):


        data = request.get_json()


        if not data:

            return {

                "message":
                    "Request body required."

            }, 400




        required_fields = [

            "category_id",
            "name",
            "sku",
            "price"

        ]



        for field in required_fields:

            if not data.get(field):

                return {

                    "message":
                        f"{field} is required."

                }, 400





        category = Category.query.get(

            data["category_id"]

        )


        if not category:

            return {

                "message":
                    "Category not found."

            }, 404





        existing = Product.query.filter_by(

            sku=data["sku"]

        ).first()



        if existing:

            return {

                "message":
                    "SKU already exists."

            }, 400





        product = Product(

            category_id=data["category_id"],

            name=data["name"],

            description=data.get(
                "description"
            ),

            sku=data["sku"],

            price=data["price"],

            stock_quantity=data.get(
                "stock_quantity",
                0
            ),

            image_url=data.get(
                "image_url"
            ),

            is_active=data.get(
                "is_active",
                True
            )

        )



        db.session.add(product)

        db.session.commit()



        return {


            "message":
                "Product created successfully.",



            "product":

            {

                "id":
                    product.id,


                "name":
                    product.name,


                "sku":
                    product.sku

            }


        }, 201







# ============================================================
# PRODUCT DETAIL
# ============================================================

class ProductDetailResource(Resource):



    # GET ONE PRODUCT

    def get(self, product_id):


        product = Product.query.get_or_404(

            product_id

        )



        return {


            "id":
                product.id,


            "category_id":
                product.category_id,


            "name":
                product.name,


            "description":
                product.description,


            "sku":
                product.sku,


            "price":
                float(product.price),


            "stock_quantity":
                product.stock_quantity,


            "image_url":
                product.image_url,


            "is_active":
                product.is_active


        }, 200







    # UPDATE PRODUCT

    def put(self, product_id):


        product = Product.query.get_or_404(

            product_id

        )


        data = request.get_json()



        if "name" in data:

            product.name = data["name"]



        if "description" in data:

            product.description = data["description"]



        if "price" in data:

            product.price = data["price"]



        if "stock_quantity" in data:

            product.stock_quantity = data["stock_quantity"]



        if "image_url" in data:

            product.image_url = data["image_url"]



        if "is_active" in data:

            product.is_active = data["is_active"]




        db.session.commit()



        return {

            "message":
                "Product updated successfully."

        }, 200







    # DELETE PRODUCT

    def delete(self, product_id):


        product = Product.query.get_or_404(

            product_id

        )


        db.session.delete(product)

        db.session.commit()



        return {

            "message":
                "Product deleted successfully."

        }, 200