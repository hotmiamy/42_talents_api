from flask import request, jsonify, abort, send_from_directory
from flask_jwt_extended import jwt_required, create_access_token
from app.models import db, Profile
from app.schemas import ProfileSchema, ValidationError, CVSchema
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf'}
profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
cv_schema = CVSchema()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_routes(app):
    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        if data.get('username') == 'test' and data.get('password') == 'test':
            access_token = create_access_token(identity='testuser')
            return jsonify({'access_token': access_token}), 200
        return jsonify({'error': 'Invalid username or password'}), 401 

    @app.route('/profiles', methods=['POST'])
    @jwt_required()
    def create_profile():
        try:
            data = profile_schema.load(request.get_json())

            new_profile = Profile(**data)

            db.session.add(new_profile)
            db.session.commit()

            return profile_schema.dump(new_profile), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

    @app.route('/profiles/<int:profile_id>/cv', methods=['POST'])
    @jwt_required()
    def upload_cv(profile_id):
        try:
            cv_schema.load({'file': request.files['file']})

            file = request.files['file']
            filename = secure_filename(file.filename)

            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            profile = db.session.get(Profile, profile_id)
            if not profile:
                abort(404, description="Profile not found")

            profile.cv_filename = filename
            db.session.commit()

            return {'message': 'File uploaded', 'filename': filename}, 200

        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except KeyError:
            return {"errors": {"file": "file is required"}}, 400

    @app.route('/profiles/<int:profile_id>/cv', methods=['GET'])
    def download_cv(profile_id):
        profile = db.session.get(Profile, profile_id)
        if not profile:
            abort(404, description="Profile not found")
        elif not profile.cv_filename:
            abort(404, description="CV not found")
        return send_from_directory(app.config['UPLOAD_FOLDER'], profile.cv_filename, as_attachment=True)

    @app.route('/profiles', methods=['GET'])
    def list_profiles():
        query = Profile.query   

        open_to_work = request.args.get('open_to_work')
        if open_to_work in ['true', 'false']:
                query = query.filter_by(open_to_work=open_to_work.lower() == 'true')

        filters = {}
        for key in request.args:
            if key.startswith('filter['):
                field = key[7:-1]
                values = request.args.get(key).split(',')
                filters[field] = values

        for field, values in filters.items():
            if field == 'skills':
                for value in values:
                    query = query.filter(Profile.skills.contains([value]))
            elif field == 'idioms':
                for value in values:
                    query = query.filter(Profile.idioms.contains(value))
            elif  field == 'locations':
                query = query.filter(Profile.location.ilike(f"%{values[0]}%"))

        profiles = query.all()
    
        return jsonify(profiles_schema.dump(profiles))
    
    @app.route('/profiles/<int:profile_id>', methods=['GET'])
    def get_profile(profile_id):
        profile = db.session.get(Profile, profile_id)

        if not profile:
            abort(404, description="Profile not found")

        return profile_schema.dump(profile)

    @app.route('/profiles/<int:profile_id>', methods=['PUT'])
    @jwt_required()
    def update_profile(profile_id):
        try:
            profile = db.session.get(Profile, profile_id)

            if not profile:
                abort(404, description="Perfil não encontrado")

            data = profile_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                if key in ['id', 'created_at']:
                  continue
                setattr(profile, key, value)
    
            db.session.commit()
            return profile_schema.dump(profile), 200
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400