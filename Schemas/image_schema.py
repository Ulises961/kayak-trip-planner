from marshmallow import Schema, fields, post_load, pre_dump, pre_load, validates, ValidationError
from Models.image import Image
import re


class ImageSchema(Schema):
    """ 
    Image Schema
    used for loading/dumping Image entities
    """

    public_id = fields.String(data_key='id', dump_only=True)
    size = fields.Float(allow_none=False, required=True, validate=lambda x: 0 < x <= 100)  # Max 100MB
    name = fields.String(allow_none=False, required=True, validate=lambda x: 1 <= len(x.strip()) <= 255)
    location = fields.String(allow_none=False, required=True, validate=lambda x: 1 <= len(x.strip()) <= 500)

    @validates('size')
    def validate_size(self, value, **kwargs):
        """Validate image size is within reasonable limits."""
        if value <= 0:
            raise ValidationError("Image size must be positive")
        if value > 100:  # 100 MB
            raise ValidationError("Image size cannot exceed 100 MB")
    
    @validates('name')
    def validate_name(self, value, **kwargs):
        """Validate and sanitize image name."""
        if not value or not value.strip():
            raise ValidationError("Image name cannot be empty")
        if len(value) > 255:
            raise ValidationError("Image name cannot exceed 255 characters")
        # Check for path traversal attempts
        if '..' in value or '/' in value or '\\' in value:
            raise ValidationError("Image name contains invalid path characters")
        # Validate file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        if not any(value.lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError(f"Image must have a valid extension: {', '.join(valid_extensions)}")
    
    @validates('location')
    def validate_location(self, value, **kwargs):
        """Validate and sanitize image location/URL."""
        if not value or not value.strip():
            raise ValidationError("Image location cannot be empty")
        if len(value) > 500:
            raise ValidationError("Image location cannot exceed 500 characters")
        # Basic URL/path validation
        if value.startswith(('http://', 'https://')):
            # URL validation
            url_pattern = re.compile(
                r'^https?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if not url_pattern.match(value):
                raise ValidationError("Invalid image URL format")
        else:
            # File path validation - prevent path traversal
            if '..' in value:
                raise ValidationError("Image location contains invalid path traversal")

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)
    
    @pre_load
    def extract_id(self, data, **kwargs):
        if "id" in data:
            data["public_id"] = data.pop("id")
        return data