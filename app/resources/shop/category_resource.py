from flask import request
from flask_restful import Resource

from app.extensions import db
from app.models.shop.category import Category


# ============================================================
# CATEGORY LIST / CREATE
# ============================================================

class CategoryResource(Resource):


    # GET ALL CATEGORIES
    def get(self):

        categories = Category.query.all()

        return [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description
            }

            for category in categories
        ], 200



    # CREATE CATEGORY
    def post(self):

        data = request.get_json()


        if not data:

            return {
                "message": "Request body required."
            }, 400



        name = data.get("name")


        if not name:

            return {
                "message": "Category name is required."
            }, 400



        existing = Category.query.filter_by(
            name=name
        ).first()


        if existing:

            return {
                "message": "Category already exists."
            }, 400



        category = Category(

            name=name,

            description=data.get(
                "description"
            )

        )


        db.session.add(category)

        db.session.commit()



        return {

            "message":
                "Category created successfully.",


            "category":
            {
                "id": category.id,
                "name": category.name,
                "description": category.description
            }

        }, 201





# ============================================================
# CATEGORY DETAIL
# ============================================================

class CategoryDetailResource(Resource):


    # GET ONE CATEGORY
    def get(self, category_id):

        category = Category.query.get_or_404(
            category_id
        )


        return {

            "id":
                category.id,

            "name":
                category.name,

            "description":
                category.description

        }, 200




    # UPDATE CATEGORY
    def put(self, category_id):

        category = Category.query.get_or_404(
            category_id
        )


        data = request.get_json()


        if "name" in data:

            category.name = data["name"]



        if "description" in data:

            category.description = data["description"]



        db.session.commit()


        return {

            "message":
                "Category updated successfully."

        }, 200





    # DELETE CATEGORY
    def delete(self, category_id):

        category = Category.query.get_or_404(
            category_id
        )


        db.session.delete(category)

        db.session.commit()


        return {

            "message":
                "Category deleted successfully."

        }, 200