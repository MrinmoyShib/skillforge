import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User, UserProfile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_users(db):
    u1 = User.objects.create_user(username="alice", email="alice@test.com", password="Pass123!")
    u2 = User.objects.create_user(username="bob", email="bob@test.com", password="Pass123!")
    u3 = User.objects.create_user(username="charlie", email="charlie@test.com", password="Pass123!")

    UserProfile.objects.create(user=u1, display_name="Alice A.", total_xp=500, problems_solved_count=5)
    UserProfile.objects.create(user=u2, display_name="Bob B.", total_xp=1000, problems_solved_count=8)
    UserProfile.objects.create(user=u3, display_name="Charlie C.", total_xp=250, problems_solved_count=10)

    return {"alice": u1, "bob": u2, "charlie": u3}


@pytest.mark.django_db
class TestLeaderboardAPI:
    def test_get_leaderboard_ordering_by_xp(self, api_client, sample_users):
        res = api_client.get("/api/v1/leaderboard/?sort=xp")
        assert res.status_code == 200
        data = res.json()
        assert data["total_count"] >= 3

        # Bob has 1000 XP -> Rank 1
        # Alice has 500 XP -> Rank 2
        # Charlie has 250 XP -> Rank 3
        top_three = data["results"][:3]
        assert top_three[0]["username"] == "bob"
        assert top_three[0]["rank"] == 1
        assert top_three[1]["username"] == "alice"
        assert top_three[1]["rank"] == 2
        assert top_three[2]["username"] == "charlie"
        assert top_three[2]["rank"] == 3

    def test_get_leaderboard_ordering_by_solved(self, api_client, sample_users):
        res = api_client.get("/api/v1/leaderboard/?sort=solved")
        assert res.status_code == 200
        data = res.json()

        # Charlie solved 10 -> Rank 1
        # Bob solved 8 -> Rank 2
        # Alice solved 5 -> Rank 3
        top_three = data["results"][:3]
        assert top_three[0]["username"] == "charlie"
        assert top_three[0]["rank"] == 1
        assert top_three[1]["username"] == "bob"
        assert top_three[1]["rank"] == 2
        assert top_three[2]["username"] == "alice"
        assert top_three[2]["rank"] == 3

    def test_leaderboard_current_user_rank(self, api_client, sample_users):
        api_client.force_authenticate(user=sample_users["alice"])
        res = api_client.get("/api/v1/leaderboard/?sort=xp")
        assert res.status_code == 200
        data = res.json()

        # Alice is rank 2
        assert data["current_user_rank"] == 2
        alice_entry = next(u for u in data["results"] if u["username"] == "alice")
        assert alice_entry["is_current_user"] is True

