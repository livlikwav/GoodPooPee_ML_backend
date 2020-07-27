from app import app

def test_hello():
    assert 1

def test_home():
    client = app.test_client()
    response = client.get('/')
    # GET /
    # HTTP Status Code: 200
    # Hello, world
    assert response.status_code == 200
    assert '{"msg" : "Hello, world"}' in str(response.data)