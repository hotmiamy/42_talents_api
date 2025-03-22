import pytest
from flask import Flask
from app.models import db, Profile
from app.app import create_app
from time import time
from io import BytesIO

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

        unique_email = f"test_{int(time())}@example.com"

        profile = Profile(
            name="Test User",
            email=unique_email,
            skills=["Python", "Flask"],
            open_to_work=True
        )
        db.session.add(profile)
        db.session.commit()
        return profile.id

# Test POST for create a profile
def test_create_profile(client):
    response = client.post('/profiles', json={
        "name": "New User",
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
    })
    assert response.status_code == 201
    assert 'id' in response.json

def test_upload_cv(client, sample_profile):
    data = {
        'file': (BytesIO(b'file content'), 'test.pdf')
    }
    response = client.post(
        f'/profiles/{sample_profile}/cv',
        data=data,
        content_type='multipart/form-data')
    
    assert response.status_code == 200
    assert 'filename' in response.json
    assert response.json['filename'] == 'test.pdf'

    profile = client.get(f'/profiles/{sample_profile}').json
    assert profile['cv_filename'] == 'test.pdf'

def test_download_cv(client, sample_profile):
    data = {
        'file': (BytesIO(b'file content'), 'test.pdf')
    }
    client.post(
        f'/profiles/{sample_profile}/cv',
        data=data,
        content_type='multipart/form-data')

    response = client.get(f'/profiles/{sample_profile}/cv')

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=test.pdf'
    assert response.data == b'file content'

def test_download_noexistent_cv(client, sample_profile):
    response = client.get(f'/profiles/{sample_profile}/cv')
    assert response.status_code == 404

def test_upload_invalid_file(client, sample_profile):
    data = {
        'file': (BytesIO(b'file content'), 'test.txt')
    }
    response = client.post(
        f'/profiles/{sample_profile}/cv',
        data=data,
        content_type='multipart/form-data')
    
    assert response.status_code == 400
    assert response.json['error'] == 'File type not allowed'

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

def test_update_profile(client, sample_profile):
    update_data = {
        "name": "Updated User",
        "skills": ["Django", "APIs", "Python"],
        "open_to_work": False,
        "bio" : "dev fullstack"
    }

    # Check if the profile was updated
    response = client.put(f'/profiles/{sample_profile}', json=update_data)
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

def test_update_noexistent_profile(client):
    response = client.put('/profiles/999', json={"name": "Ghost"})
    assert response.status_code == 404