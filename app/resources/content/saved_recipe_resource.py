from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.recipe import Recipe
from app.models.content.saved_recipe import SavedRecipe


class SavedRecipeResource(Resource):

    @jwt_required()
    def post(self, recipe_id):

        current_user_id = get_jwt_identity()

        Recipe.query.get_or_404(recipe_id)

        existing = SavedRecipe.query.filter_by(
            user_id=current_user_id,
            recipe_id=recipe_id
        ).first()

        if existing:
            return {
                "message": "Recipe already saved."
            }, 409

        saved = SavedRecipe(
            user_id=current_user_id,
            recipe_id=recipe_id
        )

        db.session.add(saved)
        db.session.commit()

        return {
            "message": "Recipe saved successfully."
        }, 201


class RemoveSavedRecipeResource(Resource):

    @jwt_required()
    def delete(self, recipe_id):

        current_user_id = get_jwt_identity()

        saved = SavedRecipe.query.filter_by(
            user_id=current_user_id,
            recipe_id=recipe_id
        ).first()

        if not saved:
            return {
                "message": "Recipe not saved."
            }, 404

        db.session.delete(saved)
        db.session.commit()

        return {
            "message": "Recipe removed from saved."
        }, 200


class UserSavedRecipesResource(Resource):

    @jwt_required()
    def get(self):

        current_user_id = get_jwt_identity()

        saved_recipes = SavedRecipe.query.filter_by(
            user_id=current_user_id
        ).all()

        recipe_list = []

        for saved in saved_recipes:

            recipe = saved.recipe

            recipe_list.append({
                "id": recipe.id,
                "title": recipe.title,
                "thumbnail": recipe.thumbnail,
                "saved_at": saved.created_at
            })

        return recipe_list, 200