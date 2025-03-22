from flask import request, jsonify, abort
from models import db, Profile
from sqlalchemy import text
import os
from werkzeurg.utils import secure_filename
from app import app

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_routes(app):
    @app.route('/profiles', methods=['POST'])
    def create_profile():
        data = request.get_json()

        if not data.get('name'):
            return {"error": "name is required"}, 400
        if not data.get('email'):
            return {"error": "email is required"}, 400

        new_profile = Profile(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            location=data.get('location'),
            linkedin_profile=data.get('linkedin_profile'),
            github_profile=data.get('github_profile'),
            skills=data.get('skills', []),
            experience=data.get('experience'),
            education=data.get('education'),
            idioms=data.get('idioms', []),
            bio=data.get('bio'),
            open_to_work=data.get('open_to_work', True)
        )

        db.session.add(new_profile)
        db.session.commit()

        return jsonify({"id": new_profile.id,
                        "name": new_profile.name,
                        "email": new_profile.email,
                        "phone": new_profile.phone,
                        "location": new_profile.location,
                        "linkedin_profile": new_profile.linkedin_profile,
                        "github_profile": new_profile.github_profile,
                        "skills": new_profile.skills,
                        "experience": new_profile.experience,
                        "education": new_profile.education,
                        "idioms": new_profile.idioms,
                        "bio": new_profile.bio,
                        "open_to_work": new_profile.open_to_work,
                        "created_at": new_profile.created_at.isoformat()
                        }), 201

    @app.route('/profiles/<int:profile_id>/cv', methods=['POST'])
    def upload_cv(profile_id):
        if 'file' not in request.files:
          return {"error": "No file part"}, 400
        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            profile = db.session.get(Profile, profile_id)
            if not profile:
                abort(404, description="Profile not found")
            profile.cv_filename = filename
            db.session.commit()
            return {'message': 'File uploaded', 'filename': filename}, 200
        else: 
            return {"error": "File type not allowed"}, 400

    @app.route('/profiles/<int:profile_id>/cv', methods=['GET'])
    def download_cv(profile_id):
        profile = db.session.get(Profile, profile_id)
        if not profile:
            abort(404, description="Profile not found")
        return send_from_directory(UPLOAD_FOLDER, profile.cv_filename, as_attachment=True)

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
                    query = query.filter(text("EXIST (SELECT 1 FROM json_each(profile.skills) WHERE value = :value)")).bindparams(value=value)
            elif field == 'idioms':
                for value in values:
                    query = query.filter(text("EXIST (SELECT 1 FROM json_each(profile.idioms) WHERE value = :value)")).bindparams(value=value)
            elif  field == 'locations':
                query = query.filter(Profile.location.ilike(f"%{values[0]}%"))

        profiles = query.all()
    
        return jsonify([{"id": profile.id,
                        "name": profile.name,
                        "email": profile.email,
                        "phone": profile.phone,
                        "location": profile.location,
                        "linkedin_profile": profile.linkedin_profile,
                        "github_profile": profile.github_profile,
                        "skills": profile.skills,
                        "experience": profile.experience,
                        "education": profile.education,
                        "idioms": profile.idioms,
                        "bio": profile.bio,
                        "open_to_work": profile.open_to_work,
                        "created_at": profile.created_at.isoformat() if profile.created_at else None
                        } for profile in profiles])
    
    @app.route('/profiles/<int:profile_id>', methods=['GET'])
    def get_profile(profile_id):
        profile = db.session.get(Profile, profile_id)

        if not profile:
            abort(404, description="Profile not found")

        return jsonify({"id": profile.id,
                        "name": profile.name,
                        "email": profile.email,
                        "phone": profile.phone,
                        "location": profile.location,
                        "linkedin_profile": profile.linkedin_profile,
                        "github_profile": profile.github_profile,
                        "skills": profile.skills,
                        "experience": profile.experience,
                        "education": profile.education,
                        "idioms": profile.idioms,
                        "bio": profile.bio,
                        "open_to_work": profile.open_to_work,
                        "created_at": profile.created_at.isoformat() if profile.created_at else None
                        })

    @app.route('/profiles/<int:profile_id>', methods=['PUT'])
    def update_profile(profile_id):
        profile = db.session.get(Profile, profile_id)

        if not profile:
            abort(404, description="Perfil não encontrado")

        data = request.get_json()

        for key, value in data.items():
            if key in ['id', 'created_at']:
                continue

            if hasattr(profile, key):
                if key == 'skills' or key == 'idioms':
                    if isinstance(value, list):
                        setattr(profile, key, value)
                    else:
                        setattr(profile, key, [value])
                else:
                    setattr(profile, key, value)
    
        db.session.commit()

        return jsonify({"id": profile.id,
                        "name": profile.name,
                        "email": profile.email,
                        "phone": profile.phone,
                        "location": profile.location,
                        "linkedin_profile": profile.linkedin_profile,
                        "github_profile": profile.github_profile,
                        "skills": profile.skills,
                        "experience": profile.experience,
                        "education": profile.education,
                        "idioms": profile.idioms,
                        "bio": profile.bio,
                        "open_to_work": profile.open_to_work,
                        "created_at": profile.created_at.isoformat() if profile.created_at else None
                        }), 200