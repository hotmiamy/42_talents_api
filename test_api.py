import pytest
from flask import Flask
from app.models import db, Profile
from app.app import create_app
from time import time
from io import BytesIO
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='function')
def app(tmpdir):
    # Cria a app de teste usando a mesma factory do app principal
    app = create_app(config_name='development')
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "UPLOAD_FOLDER": tmpdir.mkdir('uploads').strpath
    })
    
    # Cria o banco de dados dentro do contexto da app
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Limpeza (opcional para SQLite em memória)
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    # Cria um cliente de teste
    return app.test_client()

# criate a test profile to use in multiple tests
@pytest.fixture
def sample_profile(app):
    with app.app_context():
        profile = Profile(
            name="Test User",
            email=f"test_{int(time())}@example.com",
            skills=["Python", "Flask"],
            open_to_work=True,
            linkedin_profile="https://linkedin.com/test"
        )
        db.session.add(profile)
        db.session.commit()
        return profile.id
    
@pytest.fixture
def auth_headers(app):
    with app.app_context():
        access_token = create_access_token(identity='testuser')
        return {'Authorization': f'Bearer {access_token}'}

# Test POST for create a profile
def test_create_profile(client, auth_headers):
    valid_data = { "name": "New User",
        "email": "new@exaple.com",
        "phone": "123456789",
        "location": "Test City",
        "linkedin_profile": "https://www.linkedin.com/in/testuser",
        "github_profile": "https://www.github.com/in/testuser",
        "skills": ["Python", "Javascript"],
        "experience": "Test experience",
        "education": "Test education",
        "idioms": ["English", "Spanish"],
        "bio": "Test bio",
        "open_to_work": True
    }
    response = client.post('/profiles', json=valid_data, headers=auth_headers)
    assert response.status_code == 201
    assert 'id' in response.json

    # test for invalid email
    invalid_email_data = valid_data.copy()
    invalid_email_data['email'] = 'invalid-email'
    response = client.post('/profiles', json=invalid_email_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'email' in response.json['errors']

    # test for too many skills
    invalid_skills_data = valid_data.copy()
    invalid_skills_data['skills'] = [f"skills{i}" for i in range(11)]
    response = client.post('/profiles', json=invalid_skills_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'skills' in response.json['errors']

def test_upload_cv(client, sample_profile, auth_headers):
    data = {
        'file': (BytesIO(b'file content'), 'test.pdf')
    }
    response = client.post(
        f'/profiles/{sample_profile}/cv',
        data=data,
        content_type='multipart/form-data',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert 'filename' in response.json
    assert response.json['filename'] == 'test.pdf'

    profile = client.get(f'/profiles/{sample_profile}').json
    assert profile['cv_filename'] == 'test.pdf'

def test_download_cv(client, sample_profile, auth_headers):
    data = {
        'file': (BytesIO(b'file content'), 'test.pdf')
    }
    client.post(
        f'/profiles/{sample_profile}/cv',
        data=data,
        content_type='multipart/form-data',
        headers=auth_headers
    )

    response = client.get(f'/profiles/{sample_profile}/cv')

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=test.pdf'
    assert response.data == b'file content'

def test_download_noexistent_cv(client, sample_profile):
    response = client.get(f'/profiles/{sample_profile}/cv')
    assert response.status_code == 404

def test_upload_invalid_file(client, sample_profile, auth_headers):
    invalid_type_data = {
        'file': (BytesIO(b'file content'), 'test.txt')
    }
    response = client.post(
        f'/profiles/{sample_profile}/cv',
        data=invalid_type_data,
        content_type='multipart/form-data',
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert 'file' in response.json['errors']
    assert 'Only PDF files are allowed' in response.json['errors']['file'][0]

def test_upload_large_file(client, sample_profile, auth_headers):
    large_file = b'a' * (5 * 1024 * 1024 + 1)
    large_data = {
        'file': (BytesIO(large_file), 'big.pdf')
    }
    response = client.post(
        f'/profiles/{sample_profile}/cv',
        data=large_data,
        content_type='multipart/form-data',
        headers=auth_headers
    )

    assert response.status_code == 400
    assert 'file' in response.json['errors']
    assert 'exceeds 5MB' in response.json['errors']['file'][0]

# Test the get list of profiles
def test_get_all_profiles(client, sample_profile):
    response = client.get('/profiles')
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) >= 1

# Test the filters
def test_filter_profiles(client, sample_profile):
    response = client.get('/profiles?open_to_work=true')
    assert response.status_code == 200
    assert all(p['open_to_work'] is True for p in response.json)

def test_complex_filters(client, sample_profile):
    response = client.get('/profiles?filter[skills]=Python')
    assert response.status_code == 200
    assert all('Python' in p['skills'] for p in response.json)

    response = client.get('/profiles?filter[skills]=Python&open_to_work=true')
    assert response.status_code == 200
    for profile in response.json:
        assert 'Python' in profile['skills']
        assert profile['open_to_work'] is True

# Test the get a single profile
def test_get_profile(client, sample_profile):
    response = client.get(f'/profiles/{sample_profile}')
    assert response.status_code == 200
    assert response.json['id'] == sample_profile
    assert response.json['name'] == "Test User"

def test_update_profile(client, sample_profile, auth_headers):
    update_data = {
        "name": "Updated User",
        "skills": ["Django", "APIs", "Python"],
        "open_to_work": False,
        "bio" : "dev fullstack"
    }

    # Check if the profile was updated
    response = client.put(
        f'/profiles/{sample_profile}',
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json

    assert data['name'] == "Updated User"
    assert "Django" in data['skills']
    assert data['open_to_work'] is False
    assert "dev fullstack" in data['bio']

    # Check if the profile dont change other fields
    original_profile = client.get(f'/profiles/{sample_profile}').json
    assert original_profile['email'] == data['email']
    assert original_profile['created_at'] == data['created_at']

    # invalid URL for linkedin_profile
    invalid_data = {"linkedin_profile": "invalid-url"}
    response = client.put(
        f'/profiles/{sample_profile}',
        json=invalid_data,
        headers=auth_headers
    )
    assert response.status_code == 400
    assert 'linkedin_profile' in response.json['errors']

def test_update_noexistent_profile(client, auth_headers):
    response = client.put('/profiles/999', json={"name": "Ghost"}, headers=auth_headers)
    assert response.status_code == 404