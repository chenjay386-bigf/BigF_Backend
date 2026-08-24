from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.content.recipe import Recipe
from app.models.content.recipe_rating import RecipeRating


class RatingResource(Resource):

    # GET ALL RATINGS FOR A RECIPE
    def get(self, recipe_id):

        Recipe.query.get_or_404(recipe_id)

        ratings = RecipeRating.query.filter_by(
            recipe_id=recipe_id
        ).all()

        rating_list = []

        for rating in ratings:
            rating_list.append({
                "id": rating.id,
                "rating": rating.rating,
                "user_id": rating.user_id,
                "review": getattr(rating, "review", None),
                "created_at": rating.created_at.isoformat()
                if rating.created_at else None
            })

        return rating_list, 200


    # CREATE OR UPDATE RATING
    @jwt_required()
    def post(self, recipe_id):

        current_user_id = get_jwt_identity()

        Recipe.query.get_or_404(recipe_id)

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400


        rating_value = data.get("rating")

        if rating_value is None or not (1 <= int(rating_value) <= 5):
            return {
                "message": "Rating must be between 1 and 5."
            }, 400


        existing = RecipeRating.query.filter_by(
            user_id=current_user_id,
            recipe_id=recipe_id
        ).first()


        if existing:

            existing.rating = rating_value

            if hasattr(existing, "review"):
                existing.review = data.get("review")

            db.session.commit()

            return {
                "message": "Rating updated successfully.",
                "rating_id": existing.id
            }, 200


        rating = RecipeRating(
            user_id=current_user_id,
            recipe_id=recipe_id,
            rating=rating_value
        )


        if hasattr(rating, "review"):
            rating.review = data.get("review")


        db.session.add(rating)
        db.session.commit()


        return {
            "message": "Rating added successfully.",
            "rating_id": rating.id
        }, 201



class RatingDetailResource(Resource):

    # DELETE OWN RATING
    @jwt_required()
    def delete(self, rating_id):

        current_user_id = get_jwt_identity()

        rating = RecipeRating.query.get_or_404(rating_id)


        if rating.user_id != current_user_id:

            return {
                "message": "You can only delete your own ratings."
            }, 403


        db.session.delete(rating)
        db.session.commit()


        return {
            "message": "Rating deleted successfully."
        }, 200