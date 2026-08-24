from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.models.user.user import User


class AchievementResource(Resource):
    def get(self):
        return [], 200


class UserAchievementResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        User.query.get_or_404(current_user_id)
        return [], 200

