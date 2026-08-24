from flask_restful import Api


def register_resources(api: Api):

    # ============================================================
    # AUTH
    # ============================================================

    from app.resources.user.auth_resource import (
        RegisterResource,
        LoginResource,
        MeResource,
        ChangePasswordResource,
        AdminLoginResource,
    )

    api.add_resource(
        RegisterResource,
        "/auth/register"
    )

    api.add_resource(
        LoginResource,
        "/auth/login"
    )

    api.add_resource(
        MeResource,
        "/auth/me"
    )

    api.add_resource(
        ChangePasswordResource,
        "/auth/change-password"
    )

    # Admin login
    api.add_resource(
        AdminLoginResource,
        "/auth/admin-login"
    )


    # ============================================================
    # CONTENT
    # ============================================================

    from app.resources.content.ingredient_resource import (
        IngredientResource,
        IngredientDetailResource,
    )

    api.add_resource(
        IngredientResource,
        "/ingredients"
    )

    api.add_resource(
        IngredientDetailResource,
        "/ingredients/<int:ingredient_id>"
    )


    from app.resources.content.recipe_resource import (
        RecipeResource,
        RecipeDetailResource,
    )

    api.add_resource(
        RecipeResource,
        "/recipes"
    )

    api.add_resource(
        RecipeDetailResource,
        "/recipes/<int:recipe_id>"
    )


    from app.resources.content.recipe_ingredient_resource import (
        RecipeIngredientResource,
        RecipeIngredientDetailResource,
    )

    api.add_resource(
        RecipeIngredientResource,
        "/recipes/<int:recipe_id>/ingredients"
    )

    api.add_resource(
        RecipeIngredientDetailResource,
        "/recipe-ingredients/<int:recipe_ingredient_id>"
    )


    from app.resources.content.post_resource import (
        PostResource,
        PostDetailResource,
    )

    api.add_resource(
        PostResource,
        "/posts"
    )

    api.add_resource(
        PostDetailResource,
        "/posts/<int:post_id>"
    )


    from app.resources.content.media_resource import (
        MediaResource,
        MediaDetailResource,
    )

    api.add_resource(
        MediaResource,
        "/posts/<int:post_id>/media"
    )

    api.add_resource(
        MediaDetailResource,
        "/media/<int:media_id>"
    )


    from app.resources.content.comment_resource import (
        CommentResource,
        CommentDetailResource,
    )

    api.add_resource(
        CommentResource,
        "/posts/<int:post_id>/comments"
    )

    api.add_resource(
        CommentDetailResource,
        "/comments/<int:comment_id>"
    )


    from app.resources.content.like_resource import (
        LikeResource,
        UnlikeResource,
        PostLikesResource,
    )

    api.add_resource(
        LikeResource,
        "/posts/<int:post_id>/likes"
    )

    api.add_resource(
        UnlikeResource,
        "/posts/<int:post_id>/unlike"
    )

    api.add_resource(
        PostLikesResource,
        "/posts/<int:post_id>/like-list"
    )


    from app.resources.content.rating_resource import (
        RatingResource,
        RatingDetailResource,
    )

    api.add_resource(
        RatingResource,
        "/recipes/<int:recipe_id>/ratings"
    )

    api.add_resource(
        RatingDetailResource,
        "/ratings/<int:rating_id>"
    )


    from app.resources.content.saved_recipe_resource import (
        SavedRecipeResource,
        RemoveSavedRecipeResource,
        UserSavedRecipesResource,
    )

    api.add_resource(
        SavedRecipeResource,
        "/recipes/<int:recipe_id>/save"
    )

    api.add_resource(
        RemoveSavedRecipeResource,
        "/recipes/<int:recipe_id>/save"
    )

    api.add_resource(
        UserSavedRecipesResource,
        "/saved-recipes"
    )


    from app.resources.content.reshare_resource import (
        ReshareResource,
        RemoveReshareResource,
        PostResharesResource,
    )

    api.add_resource(
        ReshareResource,
        "/posts/<int:post_id>/reshare"
    )

    api.add_resource(
        RemoveReshareResource,
        "/posts/<int:post_id>/reshare"
    )

    api.add_resource(
        PostResharesResource,
        "/posts/<int:post_id>/reshares"
    )


    from app.resources.content.social_media_submission_resource import (
        SocialMediaSubmissionResource,
        SocialMediaSubmissionDetailResource,
        UserSocialMediaSubmissionsResource,
    )

    api.add_resource(
        SocialMediaSubmissionResource,
        "/social-media-submissions"
    )

    api.add_resource(
        SocialMediaSubmissionDetailResource,
        "/social-media-submissions/<int:submission_id>"
    )

    api.add_resource(
        UserSocialMediaSubmissionsResource,
        "/my-social-media-submissions"
    )


    # ============================================================
    # CHALLENGES
    # ============================================================

    from app.resources.challenges.challenge_resource import (
        ChallengeResource,
        ChallengeDetailResource,
        ChallengeParticipantsResource,
    )

    api.add_resource(
        ChallengeResource,
        "/challenges"
    )

    api.add_resource(
        ChallengeDetailResource,
        "/challenges/<int:challenge_id>"
    )

    api.add_resource(
        ChallengeParticipantsResource,
        "/challenges/<int:challenge_id>/participants"
    )


    # ============================================================
    # CHALLENGE WINNER
    # ============================================================

    from app.resources.challenges.challenge_winner_resource import (
        ChallengeWinnerResource,
    )

    api.add_resource(
        ChallengeWinnerResource,
        "/challenges/<int:challenge_id>/winner"
    )


    # ============================================================
    # CHALLENGE SUBMISSIONS
    # ============================================================

    from app.resources.challenges.challenge_submission_resource import (
        ChallengeSubmissionResource,
        ChallengeSubmissionDetailResource,
        ChallengeSubmissionsResource,
    )

    # User joins a challenge and submits their entry.
    #
    # POST
    # /challenges/<challenge_id>/submissions
    #
    # The submission now supports the TikTok link.
    api.add_resource(
        ChallengeSubmissionResource,
        "/challenges/<int:challenge_id>/submissions"
    )

    # View all submissions for a challenge.
    #
    # GET
    # /challenges/<challenge_id>/submissions
    api.add_resource(
        ChallengeSubmissionsResource,
        "/challenges/<int:challenge_id>/submissions"
    )

    # View/delete one submission.
    #
    # GET
    # DELETE
    # /challenge-submissions/<submission_id>
    api.add_resource(
        ChallengeSubmissionDetailResource,
        "/challenge-submissions/<int:submission_id>"
    )


    # ============================================================
    # CHALLENGE VOTING
    # ============================================================

    from app.resources.challenges.challenge_vote_resource import (
        ChallengeVoteResource,
        ChallengeSubmissionVotesResource,
    )

    # Vote for a challenge submission.
    #
    # POST
    # /challenge-submissions/<submission_id>/vote
    api.add_resource(
        ChallengeVoteResource,
        "/challenge-submissions/<int:submission_id>/vote"
    )

    # View votes for a submission.
    #
    # GET
    # /challenge-submissions/<submission_id>/votes
    api.add_resource(
        ChallengeSubmissionVotesResource,
        "/challenge-submissions/<int:submission_id>/votes"
    )


    # ============================================================
    # ADMIN CHALLENGE MODERATION
    # ============================================================

    from app.resources.challenges.challenge_submission_moderation_resource import (
        ChallengeSubmissionModerationResource,
        ChallengeSubmissionModerationListResource,
    )

    # ------------------------------------------------------------
    # ADMIN:
    # View submissions waiting for moderation
    #
    # GET
    # /admin/challenge-submissions/moderation
    #
    # ------------------------------------------------------------

    api.add_resource(
        ChallengeSubmissionModerationListResource,
        "/admin/challenge-submissions/moderation"
    )


    # ------------------------------------------------------------
    # ADMIN:
    # Approve / reject a submission
    #
    # GET
    # /admin/challenge-submissions/<submission_id>/moderate
    #
    # PUT
    # /admin/challenge-submissions/<submission_id>/moderate
    #
    # ------------------------------------------------------------

    api.add_resource(
        ChallengeSubmissionModerationResource,
        "/admin/challenge-submissions/<int:submission_id>/moderate"
    )


    # ============================================================
    # CHALLENGE REWARDS
    # ============================================================

    from app.resources.challenges.challenge_reward_resource import (
        ChallengeRewardResource,
        ChallengeRewardDetailResource,
        UserRewardsResource,
    )

    api.add_resource(
        ChallengeRewardResource,
        "/challenges/<int:challenge_id>/reward"
    )

    api.add_resource(
        ChallengeRewardDetailResource,
        "/challenge-rewards/<int:reward_id>"
    )

    api.add_resource(
        UserRewardsResource,
        "/my-rewards"
    )


    # ============================================================
    # SHOP - CATEGORIES
    # ============================================================

    from app.resources.shop.category_resource import (
        CategoryResource,
        CategoryDetailResource,
    )

    api.add_resource(
        CategoryResource,
        "/shop/categories"
    )

    api.add_resource(
        CategoryDetailResource,
        "/shop/categories/<int:category_id>"
    )


    # ============================================================
    # SHOP - PRODUCTS
    # ============================================================

    from app.resources.shop.product_resource import (
        ProductResource,
        ProductDetailResource,
    )

    api.add_resource(
        ProductResource,
        "/shop/products"
    )

    api.add_resource(
        ProductDetailResource,
        "/shop/products/<int:product_id>"
    )


    # ============================================================
    # SHOP - CART
    # ============================================================

    from app.resources.shop.cart_resource import (
        CartResource,
    )

    api.add_resource(
        CartResource,
        "/shop/cart/<int:user_id>"
    )


    # ============================================================
    # SHOP - CART ITEMS
    # ============================================================

    from app.resources.shop.cart_item_resource import (
        CartItemResource,
        CartItemDetailResource,
    )

    api.add_resource(
        CartItemResource,
        "/shop/cart/<int:cart_id>/items"
    )

    api.add_resource(
        CartItemDetailResource,
        "/shop/cart-item/<int:item_id>"
    )


    # ============================================================
    # SHOP - ORDERS
    # ============================================================

    from app.resources.shop.order_resource import (
        OrderResource,
        OrderDetailResource,
    )

    api.add_resource(
        OrderResource,
        "/shop/orders"
    )

    api.add_resource(
        OrderDetailResource,
        "/shop/orders/<int:order_id>"
    )


    # ============================================================
    # SHOP - DELIVERY
    # ============================================================

    from app.resources.shop.delivery_resource import (
        DeliveryResource,
        DeliveryDetailResource,
    )

    api.add_resource(
        DeliveryResource,
        "/shop/deliveries"
    )

    api.add_resource(
        DeliveryDetailResource,
        "/shop/deliveries/<int:delivery_id>"
    )


    # ============================================================
    # SHOP - PAYMENT
    # ============================================================

    from app.resources.shop.payment_resource import (
        PaymentResource,
        PaymentDetailResource,
    )

    api.add_resource(
        PaymentResource,
        "/shop/payments"
    )

    api.add_resource(
        PaymentDetailResource,
        "/shop/payments/<int:payment_id>"
    )


    # ============================================================
    # COMPLETE
    # ============================================================

    print(
        "API resources registered successfully."
    )