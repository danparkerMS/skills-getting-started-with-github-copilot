from fastapi.testclient import TestClient


def test_signup_adds_participant(client: TestClient) -> None:
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/Art Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Art Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Art Club"]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client: TestClient) -> None:
    response = client.post("/activities/NotAClub/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client: TestClient) -> None:
    existing_email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={existing_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
