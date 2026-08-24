
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.recipe import Recipe


class RecipeResource(Resource):

    # GET ALL RECIPES
    def get(self):

        recipes = Recipe.query.filter_by(
            status="published"
        ).all()

        recipe_list = []

        for recipe in recipes:

            recipe_list.append({
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "thumbnail": recipe.thumbnail,
                "cooking_time": recipe.cooking_time,
                "servings": recipe.servings,
                "difficulty": recipe.difficulty,
                "views": recipe.views,

                "creator": {
                    "id": recipe.user.id,
                    "username": recipe.user.username
                },

                "created_at": (
                    recipe.created_at.isoformat()
                    if recipe.created_at
                    else None
                ),

                "updated_at": (
                    recipe.updated_at.isoformat()
                    if recipe.updated_at
                    else None
                )
            })

        return recipe_list, 200


    # CREATE RECIPE
    @jwt_required()
    def post(self):

        current_user_id = int(get_jwt_identity())

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        if not data.get("title"):
            return {
                "message": "Recipe title is required."
            }, 400

        if not data.get("instructions"):
            return {
                "message": "Recipe instructions are required."
            }, 400

        recipe = Recipe(
            user_id=current_user_id,
            title=data["title"],
            description=data.get("description"),
            instructions=data["instructions"],
            thumbnail=data.get("thumbnail"),
            cooking_time=data.get("cooking_time"),
            servings=data.get("servings"),
            difficulty=data.get("difficulty", "Easy")
        )

        db.session.add(recipe)
        db.session.commit()

        return {
            "message": "Recipe created successfully.",
            "recipe_id": recipe.id
        }, 201


class RecipeDetailResource(Resource):

    # GET SINGLE RECIPE
    def get(self, recipe_id):

        recipe = Recipe.query.get_or_404(recipe_id)

        # Increase recipe views
        recipe.views += 1

        db.session.commit()

        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "instructions": recipe.instructions,
            "thumbnail": recipe.thumbnail,
            "cooking_time": recipe.cooking_time,
            "servings": recipe.servings,
            "difficulty": recipe.difficulty,
            "views": recipe.views,

            "creator": {
                "id": recipe.user.id,
                "username": recipe.user.username
            },

            "created_at": (
                recipe.created_at.isoformat()
                if recipe.created_at
                else None
            ),

            "updated_at": (
                recipe.updated_at.isoformat()
                if recipe.updated_at
                else None
            )
        }, 200


    # UPDATE RECIPE
    @jwt_required()
    def put(self, recipe_id):

        current_user_id = int(get_jwt_identity())

        recipe = Recipe.query.get_or_404(recipe_id)

        # Only the recipe owner can update it
        if recipe.user_id != current_user_id:

            return {
                "message": "You can only update your own recipes."
            }, 403

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        recipe.title = data.get(
            "title",
            recipe.title
        )

        recipe.description = data.get(
            "description",
            recipe.description
        )

        recipe.instructions = data.get(
            "instructions",
            recipe.instructions
        )

        recipe.thumbnail = data.get(
            "thumbnail",
            recipe.thumbnail
        )

        recipe.cooking_time = data.get(
            "cooking_time",
            recipe.cooking_time
        )

        recipe.servings = data.get(
            "servings",
            recipe.servings
        )

        recipe.difficulty = data.get(
            "difficulty",
            recipe.difficulty
        )

        recipe.status = data.get(
            "status",
            recipe.status
        )

        db.session.commit()

        return {
            "message": "Recipe updated successfully."
        }, 200


    # DELETE RECIPE
    @jwt_required()
    def delete(self, recipe_id):

        current_user_id = int(get_jwt_identity())

        recipe = Recipe.query.get_or_404(recipe_id)

        # Only the recipe owner can delete it
        if recipe.user_id != current_user_id:

            return {
                "message": "You can only delete your own recipes."
            }, 403

        db.session.delete(recipe)
        db.session.commit()

        return {
            "message": "Recipe deleted successfully."
        }, 200
