from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from flask import current_app
from werkzeug.utils import secure_filename
import os

class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(validate=validate.Length(max=20))
    location = fields.Str(validate=validate.Length(max=100))
    linkedin_profile = fields.Url(relative=False)
    github_profile = fields.Url(relative=False)
    skills = fields.List(fields.Str(), load_default=[])
    experience = fields.Str()
    education = fields.Str()
    idioms = fields.List(fields.Str(), load_default=[])
    bio = fields.Str()
    open_to_work = fields.Boolean(load_default=True)
    cv_filename = fields.Str(dump_only=True) 
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_skills(self, data, **kwargs):
        skills = data.get('skills', [])
        if len(skills) > 10:
            raise ValidationError('Skills must have at most 10 items', 'skills')
        
    @validates_schema
    def validate_idioms(self, data, **kwargs):
        idioms = data.get('idioms',[])
        if len(idioms) > 5:
            raise ValidationError('Idioms must have at most 5 items', 'idioms')
        
class CVSchema(Schema):
    file = fields.Raw(required=True)

    @validates_schema
    def validate_file(self, data, **kwargs):
        file = data.get('file')

        if not file:
            raise ValidationError("file is required", "file")

        filename = secure_filename(file.filename)
        if not (filename and filename.lower().endswith('.pdf')):
            raise ValidationError("Only PDF files are allowed", "file")
        
        max_size = current_app.config.get('CV_MAX_SIZE', 5 * 1024 * 1024)
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > max_size:
            mb = max_size // (1024 * 1024)
            raise ValidationError(f"File exceeds {mb}MB", "file")