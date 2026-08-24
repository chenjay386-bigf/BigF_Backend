# ============================================================
# USER MODELS
# ============================================================

from app.models.user.user import User
from app.models.user.profile import Profile
from app.models.user.follow import Follow


# ============================================================
# CONTENT MODELS
# ============================================================

from app.models.content.recipe import Recipe
from app.models.content.ingredient import Ingredient
from app.models.content.recipe_ingredient import RecipeIngredient

from app.models.content.post import Post
from app.models.content.media import Media
from app.models.content.comment import Comment
from app.models.content.like import Like

from app.models.content.recipe_rating import RecipeRating

from app.models.content.saved_recipe import SavedRecipe
from app.models.content.reshare import Reshare

from app.models.content.social_media_submission import (
    SocialMediaSubmission
)


# ============================================================
# CHALLENGE MODELS
# ============================================================

from app.models.challenges.challenge import Challenge

from app.models.challenges.challenge_submission import (
    ChallengeSubmission
)

from app.models.challenges.challenge_vote import (
    ChallengeVote
)

from app.models.challenges.challenge_reward import (
    ChallengeReward
)


# ============================================================
# SHOP MODELS
# ============================================================

from app.models.shop.category import Category
from app.models.shop.product import Product

from app.models.shop.cart import Cart
from app.models.shop.cart_item import CartItem

from app.models.shop.order import Order
from app.models.shop.order_item import OrderItem

from app.models.shop.delivery import Delivery
from app.models.shop.payment import Payment

from app.models.shop.product_recipe import ProductRecipe


# ============================================================
# EXPORT LIST
# ============================================================

__all__ = [

    # Users
    "User",
    "Profile",
    "Follow",


    # Content
    "Recipe",
    "Ingredient",
    "RecipeIngredient",
    "Post",
    "Media",
    "Comment",
    "Like",
    "RecipeRating",
    "SavedRecipe",
    "Reshare",
    "SocialMediaSubmission",


    # Challenges
    "Challenge",
    "ChallengeSubmission",
    "ChallengeVote",
    "ChallengeReward",


    # Shop
    "Category",
    "Product",
    "Cart",
    "CartItem",
    "Order",
    "OrderItem",
    "Delivery",
    "Payment",
    "ProductRecipe",
]