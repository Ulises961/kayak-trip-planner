from marshmallow import Schema, fields, pre_load


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class BaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """
    id = fields.UUID(allow_none=True)
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @pre_load
    def snake_to_camel_input(self, data, **kwargs):
        """Convert incoming snake_case keys to camelCase before loading,
        so Marshmallow can match them to the data_key."""
        return {camelcase(k): v for k, v in data.items()}