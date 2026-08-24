from app.extensions import ma

from app.models.user.profile import Profile


class ProfileSchema(ma.SQLAlchemyAutoSchema):

    class Meta:

        model = Profile

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )


profile_schema = ProfileSchema()

profiles_schema = ProfileSchema(
    many=True
)