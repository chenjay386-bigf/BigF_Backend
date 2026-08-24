from app import create_app
from app.models.user.user import User

app = create_app()

with app.app_context():
    users = User.query.all()

    for user in users:
        print(
            user.id,
            user.username,
            user.email,
            user.role
        )

