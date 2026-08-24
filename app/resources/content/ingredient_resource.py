from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.content.ingredient import Ingredient


class IngredientResource(Resource):

    # ============================================================
    # GET ALL INGREDIENTS
    # ============================================================

    def get(self):

        ingredients = Ingredient.query.order_by(
            Ingredient.name.asc()
        ).all()

        ingredient_list = []

        for ingredient in ingredients:
            ingredient_list.append({
                "id": ingredient.id,
                "name": ingredient.name
            })

        return ingredient_list, 200

    # ============================================================
    # CREATE INGREDIENT
    # ============================================================

    @jwt_required()
    def post(self):

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        name = data.get("name")

        if not name:
            return {
                "message": "Ingredient name is required."
            }, 400

        name = name.strip()

        if not name:
            return {
                "message": "Ingredient name cannot be empty."
            }, 400

        existing = Ingredient.query.filter_by(
            name=name
        ).first()

        if existing:
            return {
                "message": "Ingredient already exists.",
                "ingredient_id": existing.id
            }, 409

        ingredient = Ingredient(
            name=name
        )

        db.session.add(ingredient)
        db.session.commit()

        return {
            "message": "Ingredient created successfully.",
            "ingredient_id": ingredient.id
        }, 201


class IngredientDetailResource(Resource):

    # ============================================================
    # GET SINGLE INGREDIENT
    # ============================================================

    def get(self, ingredient_id):

        ingredient = Ingredient.query.get_or_404(
            ingredient_id
        )

        return {
            "id": ingredient.id,
            "name": ingredient.name
        }, 200

    # ============================================================
    # UPDATE INGREDIENT
    # ============================================================

    @jwt_required()
    def put(self, ingredient_id):

        ingredient = Ingredient.query.get_or_404(
            ingredient_id
        )

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        name = data.get("name")

        if name is not None:

            name = name.strip()

            if not name:
                return {
                    "message": "Ingredient name cannot be empty."
                }, 400

            existing = Ingredient.query.filter(
                Ingredient.name == name,
                Ingredient.id != ingredient.id
            ).first()

            if existing:
                return {
                    "message": "Ingredient already exists.",
                    "ingredient_id": existing.id
                }, 409

            ingredient.name = name

        db.session.commit()

        return {
            "message": "Ingredient updated successfully."
        }, 200

    # ============================================================
    # DELETE INGREDIENT
    # ============================================================

    @jwt_required()
    def delete(self, ingredient_id):

        ingredient = Ingredient.query.get_or_404(
            ingredient_id
        )

        db.session.delete(ingredient)
        db.session.commit()

        return {
            "message": "Ingredient deleted successfully."
        }, 200