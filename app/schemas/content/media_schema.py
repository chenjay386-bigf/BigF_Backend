from app.extensions import ma

from app.models.content.media import Media


class MediaSchema(ma.SQLAlchemyAutoSchema):

    class Meta:

        model = Media

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at",
            "updated_at"
        )


media_schema = MediaSchema()

media_list_schema = MediaSchema(
    many=True
)