from app import app

def test_home():
    # Create a test client
    client = app.test_client()
    response = client.get('/')
    
    # Check that the status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response contains the expected text
    assert b"Flask is working." in response.data