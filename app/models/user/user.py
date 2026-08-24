from datetime import datetime, timezone

from flask_bcrypt import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user",
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    is_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # --------------------------
    # Relationships
    # --------------------------

    # One user has one profile
    profile = db.relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Users this user follows
    following = db.relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan"
    )

    # Users following this user
    followers = db.relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan"
    )

    # Recipes created by this user
    recipes = db.relationship(
        "Recipe",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Posts created by this user
    posts = db.relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Comments written by this user
    comments = db.relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Likes made by this user
    likes = db.relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Ratings made by this user
    recipe_ratings = db.relationship(
        "RecipeRating",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Recipes saved by this user
    saved_recipes = db.relationship(
        "SavedRecipe",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Social media submissions
    social_media_submissions = db.relationship(
        "SocialMediaSubmission",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Reshared posts
    reshares = db.relationship(
        "Reshare",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Challenges created by this user
    created_challenges = db.relationship(
        "Challenge",
        back_populates="creator",
        cascade="all, delete-orphan"
    )

    # Challenge submissions
    challenge_submissions = db.relationship(
        "ChallengeSubmission",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Votes made by this user
    challenge_votes = db.relationship(
        "ChallengeVote",
        back_populates="user"
    )

    # Rewards received
    challenge_rewards = db.relationship(
        "ChallengeReward",
        back_populates="user"
    )

    # Shopping cart (one per user)
    cart = db.relationship(
        "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Orders placed by this user
    orders = db.relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # --------------------------
    # Password Methods
    # --------------------------

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --------------------------
    # Utility Methods
    # --------------------------

    def update_last_login(self):
        self.last_login = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<User {self.username}>"
