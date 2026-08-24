from marshmallow import fields

from app.extensions import ma

from app.models.content.reshare import Reshare


class ReshareSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        attribute="user.username",
        dump_only=True
    )

    class Meta:

        model = Reshare

        load_instance = True

        include_fk = True

        ordered = True

        dump_only = (
            "id",
            "created_at"
        )


reshare_schema = ReshareSchema()

reshares_schema = ReshareSchema(
    many=True
)