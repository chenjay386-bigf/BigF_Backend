
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.extensions import db

from app.models.content.recipe import Recipe
from app.models.content.ingredient import Ingredient
from app.models.content.recipe_ingredient import RecipeIngredient


class RecipeIngredientResource(Resource):

    # ============================================================
    # GET ALL INGREDIENTS FOR A RECIPE
    # ============================================================

    def get(self, recipe_id):

        recipe = Recipe.query.get_or_404(recipe_id)

        recipe_ingredients = RecipeIngredient.query.filter_by(
            recipe_id=recipe.id
        ).all()

        ingredient_list = []

        for recipe_ingredient in recipe_ingredients:

            ingredient = recipe_ingredient.ingredient

            ingredient_list.append({
                "id": recipe_ingredient.id,
                "ingredient": {
                    "id": ingredient.id,
                    "name": ingredient.name,
                },
                "quantity": recipe_ingredient.quantity,
                "unit": recipe_ingredient.unit,
            })

        return ingredient_list, 200

    # ============================================================
    # ADD INGREDIENT TO RECIPE
    # ============================================================

    @jwt_required()
    def post(self, recipe_id):

        current_user_id = int(get_jwt_identity())

        recipe = Recipe.query.get_or_404(recipe_id)

        # Only recipe creator can add ingredients
        if recipe.user_id != current_user_id:
            return {
                "message": (
                    "You can only add ingredients to your own recipes."
                )
            }, 403

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        ingredient_id = data.get("ingredient_id")
        quantity = data.get("quantity")
        unit = data.get("unit")

        if not ingredient_id:
            return {
                "message": "ingredient_id is required."
            }, 400

        ingredient = Ingredient.query.get(ingredient_id)

        if not ingredient:
            return {
                "message": "Ingredient not found."
            }, 404

        # Prevent duplicate ingredient in the same recipe
        existing = RecipeIngredient.query.filter_by(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
        ).first()

        if existing:
            return {
                "message": (
                    "This ingredient is already added to the recipe."
                )
            }, 409

        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=quantity,
            unit=unit,
        )

        db.session.add(recipe_ingredient)
        db.session.commit()

        return {
            "message": "Ingredient added to recipe successfully.",
            "recipe_ingredient_id": recipe_ingredient.id,
        }, 201


class RecipeIngredientDetailResource(Resource):

    # ============================================================
    # GET SINGLE RECIPE INGREDIENT
    # ============================================================

    def get(self, recipe_ingredient_id):

        recipe_ingredient = RecipeIngredient.query.get_or_404(
            recipe_ingredient_id
        )

        ingredient = recipe_ingredient.ingredient

        return {
            "id": recipe_ingredient.id,
            "recipe_id": recipe_ingredient.recipe_id,
            "ingredient": {
                "id": ingredient.id,
                "name": ingredient.name,
            },
            "quantity": recipe_ingredient.quantity,
            "unit": recipe_ingredient.unit,
        }, 200

    # ============================================================
    # UPDATE RECIPE INGREDIENT
    # ============================================================

    @jwt_required()
    def put(self, recipe_ingredient_id):

        current_user_id = int(get_jwt_identity())

        recipe_ingredient = RecipeIngredient.query.get_or_404(
            recipe_ingredient_id
        )

        recipe = Recipe.query.get_or_404(
            recipe_ingredient.recipe_id
        )

        # Only recipe owner can update ingredients
        if recipe.user_id != current_user_id:
            return {
                "message": (
                    "You can only update ingredients in your own recipes."
                )
            }, 403

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        recipe_ingredient.quantity = data.get(
            "quantity",
            recipe_ingredient.quantity,
        )

        recipe_ingredient.unit = data.get(
            "unit",
            recipe_ingredient.unit,
        )

        # Allow changing the ingredient
        if "ingredient_id" in data:

            ingredient_id = data.get("ingredient_id")

            ingredient = Ingredient.query.get(ingredient_id)

            if not ingredient:
                return {
                    "message": "Ingredient not found."
                }, 404

            # Prevent duplicate ingredient
            existing = RecipeIngredient.query.filter(
                RecipeIngredient.recipe_id == recipe.id,
                RecipeIngredient.ingredient_id == ingredient.id,
                RecipeIngredient.id != recipe_ingredient.id,
            ).first()

            if existing:
                return {
                    "message": (
                        "This ingredient is already added to the recipe."
                    )
                }, 409

            recipe_ingredient.ingredient_id = ingredient.id

        db.session.commit()

        return {
            "message": "Recipe ingredient updated successfully."
        }, 200

    # ============================================================
    # DELETE INGREDIENT FROM RECIPE
    # ============================================================

    @jwt_required()
    def delete(self, recipe_ingredient_id):

        current_user_id = int(get_jwt_identity())

        recipe_ingredient = RecipeIngredient.query.get_or_404(
            recipe_ingredient_id
        )

        recipe = Recipe.query.get_or_404(
            recipe_ingredient.recipe_id
        )

        # Only recipe owner can delete ingredients
        if recipe.user_id != current_user_id:
            return {
                "message": (
                    "You can only remove ingredients from your own recipes."
                )
            }, 403

        db.session.delete(recipe_ingredient)
        db.session.commit()

        return {
            "message": "Ingredient removed from recipe successfully."
        }, 200
