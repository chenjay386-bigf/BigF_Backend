from marshmallow import fields

from app.extensions import ma
from app.models.shop.category import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):

    product_count = fields.Method(
        "get_product_count"
    )

    class Meta:

        model = Category

        load_instance = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )

    def get_product_count(self, obj):

        return len(obj.products)


category_schema = CategorySchema()

categories_schema = CategorySchema(
    many=True
)