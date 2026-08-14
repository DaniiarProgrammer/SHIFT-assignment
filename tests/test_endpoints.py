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
    client.post("/rooms/", json={"name": "1room", "capacity": 1})
    client.post("/slots/", json={"start_time": "5:00", "end_time": "16:00"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/bookings/", json={"room_id": 1, "slot_id": 1, "date": "28.07.2026"}, headers=headers)
    assert response.status_code == 201

def test_get_room_by_id_success(client):
    response_create = client.post("/rooms/", json={"name": "Room 1", "capacity": 10})
    room_id = response_create.json()["id"]
    response_get = client.get(f"/rooms/{room_id}")
    assert response_get.status_code == 200
    assert response_get.json()["name"] == "Room 1"

def test_get_room_by_id_not_found(client):
    response = client.get(f"/rooms/999")
    assert response.status_code == 404

def test_delete_room_success(client):
    response_create = client.post("/rooms/", json={"name": "Room 1", "capacity": 10})
    room_id = response_create.json()["id"]
    response_delete = client.delete(f"/rooms/{room_id}")
    assert response_delete.status_code == 204
    response_get = client.get(f"/rooms/{room_id}")
    assert response_get.status_code == 404

def test_update_room_success(client):
    response_create = client.post("/rooms/", json={"name": "Room 1", "capacity": 10})
    room_id = response_create.json()["id"]
    response_update = client.put(f"/rooms/{room_id}", json={"name": "New Room", "capacity": 100})
    assert response_update.status_code == 200
    response_get = client.get(f"/rooms/{room_id}")
    assert response_get.json()["name"] == "New Room"
    assert response_get.json()["capacity"] == 100