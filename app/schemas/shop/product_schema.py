from marshmallow import fields

from app.extensions import ma
from app.models.shop.product import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):

    category_name = fields.String(
        attribute="category.name",
        dump_only=True
    )

    linked_recipe_count = fields.Method(
        "get_linked_recipe_count"
    )

    in_stock = fields.Method(
        "get_in_stock"
    )

    class Meta:

        model = Product

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )

    def get_linked_recipe_count(self, obj):

        return len(obj.recipe_links)

    def get_in_stock(self, obj):

        return obj.stock_quantity > 0


product_schema = ProductSchema()

products_schema = ProductSchema(
    many=True
)