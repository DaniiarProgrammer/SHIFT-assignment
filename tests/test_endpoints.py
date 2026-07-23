def test_create_user(client):
    response = client.post("/users/", json={"username": "testuser", "role": "admin", "password": "testpass"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_success(client):
    client.post("/users/", json={"username": "testuser", "role": "admin", "password": "testpass"})
    response = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    # Создаём юзера
    client.post("/users/", json={"username": "wronguser", "role": "admin", "password": "correctpass"})    
    response = client.post("/auth/login", data={"username": "wronguser", "password": "wrongpass"})    
    assert response.status_code == 401

def test_delete_booking_unauthorized(client):
    response = client.delete("/bookings/1")
    assert response.status_code == 401

def test_create_booking_authorized(client):
    client.post("/users/", json={"username": "testuser", "role": "admin", "password": "testpass"})
    login_response = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    client.post("/rooms/", json={"name": "1room", "capacity": "1"})
    client.post("/slots/", json={"start_time": "5:00", "end_time": "16:00"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/bookings/", json={"room_id": 1, "slot_id": 1, "date": "28.07.2026"}, headers=headers)
    assert response.status_code == 201