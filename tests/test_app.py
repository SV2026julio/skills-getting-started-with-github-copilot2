import pytest


pytestmark = pytest.mark.anyio


async def test_get_activities_returns_data_and_cache_control_header(client):
    response = await client.get("/activities")

    assert response.status_code == 200
    assert response.headers.get("cache-control") == "no-store"

    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


async def test_signup_success_registers_participant(client):
    activity_name = "Science Club"
    email = "new.student@mergington.edu"

    response = await client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = await client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


async def test_signup_returns_404_for_unknown_activity(client):
    response = await client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


async def test_signup_returns_400_for_duplicate_participant(client):
    response = await client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


async def test_signup_returns_400_when_activity_is_full(client):
    activity_name = "Tennis Club"
    max_participants = 10
    # Fill the activity to capacity before attempting signup.
    from src.app import activities

    activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]

    response = await client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "late.student@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}


async def test_unregister_success_removes_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = await client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = await client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


async def test_unregister_returns_404_for_non_registered_participant(client):
    response = await client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not.registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not registered for this activity"}


async def test_unregister_returns_404_for_unknown_activity(client):
    response = await client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
