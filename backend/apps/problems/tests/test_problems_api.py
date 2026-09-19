"""
API and unit tests for coding problems, filtering, test cases, and admin controls.
"""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.services.auth_services import user_register, user_generate_tokens
from apps.problems.models import Category, Tag, Problem, TestCase


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_client(db):
    client = APIClient()
    admin_user = user_register(
        username="testadmin",
        email="admin@test.local",
        password="AdminPassword123!",
        display_name="Admin",
        is_active=True
    )
    admin_user.is_staff = True
    admin_user.save(update_fields=['is_staff'])

    access_token, _ = user_generate_tokens(user=admin_user)
    client.cookies['access_token'] = access_token
    return client


@pytest.fixture
def student_client(db):
    client = APIClient()
    student_user = user_register(
        username="teststudent",
        email="student@test.local",
        password="StudentPassword123!",
        display_name="Student",
        is_active=True
    )
    access_token, _ = user_generate_tokens(user=student_user)
    client.cookies['access_token'] = access_token
    return client


@pytest.fixture
def setup_problem(db):
    cat = Category.objects.create(name="Binary Search", slug="binary-search")
    tag = Tag.objects.create(name="Divide & Conquer", slug="divide-conquer")

    prob = Problem.objects.create(
        title="Find Target Index",
        slug="find-target-index",
        description="Search for target in sorted array.",
        difficulty="easy",
        challenge_level=1,
        category=cat,
        xp_reward=50,
        starter_code="// code",
        is_published=True
    )
    prob.tags.add(tag)

    sample_case = TestCase.objects.create(
        problem=prob,
        input_data="1 2 3\n2",
        expected_output="1",
        is_sample=True,
        order=1
    )
    hidden_case = TestCase.objects.create(
        problem=prob,
        input_data="1 2 3\n99",
        expected_output="-1",
        is_sample=False,
        order=2
    )

    return prob, cat, tag, sample_case, hidden_case


@pytest.mark.django_db
class TestProblemsAPI:
    def test_list_published_problems(self, api_client, setup_problem):
        prob, _, _, _, _ = setup_problem
        # Create an unpublished problem
        Problem.objects.create(
            title="Secret Draft",
            slug="secret-draft",
            description="Draft",
            difficulty="hard",
            challenge_level=5,
            category=prob.category,
            is_published=False
        )

        url = reverse('problem-list')
        response = api_client.get(url)
        assert response.status_code == 200
        slugs = [p['slug'] for p in response.data['results']]
        assert "find-target-index" in slugs
        assert "secret-draft" not in slugs

    def test_filter_by_difficulty(self, api_client, setup_problem):
        url = reverse('problem-list')
        response = api_client.get(url, {'difficulty': 'easy'})
        assert response.status_code == 200
        for p in response.data['results']:
            assert p['difficulty'] == 'easy'

    def test_filter_by_category_slug(self, api_client, setup_problem):
        url = reverse('problem-list')
        response = api_client.get(url, {'category': 'binary-search'})
        assert response.status_code == 200
        assert len(response.data['results']) >= 1
        assert response.data['results'][0]['category']['slug'] == 'binary-search'

    def test_search_by_keyword(self, api_client, setup_problem):
        url = reverse('problem-list')
        response = api_client.get(url, {'search': 'Target Index'})
        assert response.status_code == 200
        assert len(response.data['results']) >= 1
        assert response.data['results'][0]['slug'] == 'find-target-index'

    def test_public_detail_excludes_hidden_test_cases(self, api_client, setup_problem):
        prob, _, _, sample_case, hidden_case = setup_problem
        url = reverse('problem-detail', kwargs={'slug': prob.slug})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['slug'] == prob.slug

        sample_cases = response.data['sample_test_cases']
        sample_ids = [c['id'] for c in sample_cases]

        # Public response must contain sample case and NOT hidden case
        assert sample_case.id in sample_ids
        assert hidden_case.id not in sample_ids
        assert 'test_cases' not in response.data

    def test_problem_not_found(self, api_client):
        url = reverse('problem-detail', kwargs={'slug': 'non-existent-problem'})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_categories_list_with_counts(self, api_client, setup_problem):
        url = reverse('category-list')
        response = api_client.get(url)
        assert response.status_code == 200
        cat_slugs = [c['slug'] for c in response.data]
        assert 'binary-search' in cat_slugs

    def test_student_cannot_access_admin_crud(self, student_client, setup_problem):
        prob, _, _, _, _ = setup_problem
        url = reverse('admin-problem-list-create')
        response = student_client.get(url)
        assert response.status_code == 403

        delete_url = reverse('admin-problem-detail', kwargs={'problem_id': prob.id})
        del_response = student_client.delete(delete_url)
        assert del_response.status_code == 403

    def test_admin_can_view_all_test_cases(self, admin_client, setup_problem):
        prob, _, _, sample_case, hidden_case = setup_problem
        url = reverse('admin-problem-detail', kwargs={'problem_id': prob.id})
        response = admin_client.get(url)
        assert response.status_code == 200

        all_case_ids = [c['id'] for c in response.data['test_cases']]
        assert sample_case.id in all_case_ids
        assert hidden_case.id in all_case_ids

    def test_admin_create_problem(self, admin_client, setup_problem):
        _, cat, tag, _, _ = setup_problem
        url = reverse('admin-problem-list-create')
        payload = {
            "title": "Merge Sorted Lists",
            "description": "Merge two lists into one.",
            "difficulty": "medium",
            "challenge_level": 2,
            "category_id": cat.id,
            "tag_ids": [tag.id],
            "xp_reward": 100,
            "is_published": True
        }
        response = admin_client.post(url, data=payload, format='json')
        assert response.status_code == 201
        assert response.data['title'] == "Merge Sorted Lists"
        assert response.data['slug'] == "merge-sorted-lists"

