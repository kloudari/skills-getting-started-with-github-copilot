from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    target_url = "/"

    # Act
    response = client.get(target_url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    target_url = "/activities"

    # Act
    response = client.get(target_url)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert payload["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    target_url = f"/activities/{activity_name}/signup"

    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.post(target_url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "new.student@mergington.edu"
    target_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(target_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_when_student_already_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    target_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(target_url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_removes_student_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    target_url = f"/activities/{activity_name}/unregister"

    assert email in activities[activity_name]["participants"]

    # Act
    response = client.post(target_url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "student@mergington.edu"
    target_url = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(target_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_404_when_student_is_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "absent.student@mergington.edu"
    target_url = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(target_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found in this activity"}