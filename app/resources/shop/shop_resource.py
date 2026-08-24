from flask_restful import Resource

from app.models.shop.product import Product
from app.models.shop.category import Category

from app.schemas.shop.category_schema import categories_schema
from app.schemas.shop.product_schema import product_schema, products_schema


class ShopResource(Resource):

    def get(self):
        """
        Get all available BIG F products
        """

        products = Product.query.filter_by(
            is_active=True
        ).all()

        return {
            "products": products_schema.dump(products)
        }, 200


class ProductDetailResource(Resource):

    def get(self, product_id):
        """
        Get single product details
        """

        product = Product.query.get_or_404(product_id)

        return {
            "product": product_schema.dump(product)
        }, 200


class CategoryResource(Resource):

    def get(self):
        """
        Get all product categories
        """

        categories = Category.query.all()

        return {
            "categories": categories_schema.dump(categories)
        }, 200