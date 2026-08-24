from sqlalchemy.exc import SQLAlchemyError

from app import create_app
from app.extensions import bcrypt, db
from app.models.shop.category import Category
from app.models.shop.product import Product
from app.models.user.user import User


app = create_app()


def seed_database():
    with app.app_context():

        print("Starting database seeding...")

        # -------------------------------------------------
        # 1. CREATE TEST USER
        # -------------------------------------------------

        existing_user = User.query.filter_by(
            email="admin@bigf.com"
        ).first()

        if not existing_user:

            hashed_password = bcrypt.generate_password_hash(
                "Admin@123"
            ).decode("utf-8")

            admin = User(
                username="bigf_admin",
                email="admin@bigf.com",
                password=hashed_password
            )

            db.session.add(admin)

            print("Admin user created.")

        else:

            admin = existing_user

            print("Admin user already exists.")

        # -------------------------------------------------
        # 2. CREATE CATEGORIES
        # -------------------------------------------------

        categories_data = [
            {
                "name": "Instant Noodles",
                "description": "BIG F instant noodle products."
            },
            {
                "name": "Noodle Flavors",
                "description": "Different BIG F noodle flavors."
            }
        ]

        categories = {}

        for data in categories_data:

            category = Category.query.filter_by(
                name=data["name"]
            ).first()

            if not category:

                category = Category(
                    name=data["name"],
                    description=data["description"]
                )

                db.session.add(category)

                print(
                    f"Category created: {data['name']}"
                )

            categories[data["name"]] = category

        # -------------------------------------------------
        # 3. CREATE PRODUCTS
        # -------------------------------------------------

        products_data = [
            {
                "name": "BIG F Chicken Flavor Noodles",
                "sku": "BIGF-CHICKEN-70G",
                "description": "BIG F Fried Instant Noodles - Chicken Flavor.",
                "price": 50.00,
                "stock_quantity": 1000,
                "category": "Instant Noodles"
            },
            {
                "name": "BIG F Beef Flavor Noodles",
                "sku": "BIGF-BEEF-70G",
                "description": "BIG F Fried Instant Noodles - Beef Flavor.",
                "price": 50.00,
                "stock_quantity": 1000,
                "category": "Instant Noodles"
            },
            {
                "name": "BIG F Spicy Noodles",
                "sku": "BIGF-SPICY-70G",
                "description": "BIG F Fried Instant Noodles - Spicy Flavor.",
                "price": 50.00,
                "stock_quantity": 1000,
                "category": "Noodle Flavors"
            }
        ]

        for data in products_data:

            existing_product = Product.query.filter_by(
                sku=data["sku"]
            ).first()

            if not existing_product:

                product = Product(
                    name=data["name"],
                    sku=data["sku"],
                    description=data["description"],
                    price=data["price"],
                    stock_quantity=data["stock_quantity"],
                    category=categories[data["category"]]
                )

                db.session.add(product)

                print(
                    f"Product created: {data['name']}"
                )

            else:

                print(
                    f"Product already exists: {data['name']}"
                )

        # -------------------------------------------------
        # 4. SAVE CHANGES
        # -------------------------------------------------

        try:

            db.session.commit()

            print("\nDatabase seeded successfully!")

        except SQLAlchemyError as e:

            db.session.rollback()

            print(
                f"\nError while seeding database: {e}"
            )


if __name__ == "__main__":
    seed_database()
