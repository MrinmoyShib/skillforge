"""
Integration tests for Code Submissions, Sandbox Evaluation, Anti-Farming XP, and Security Sanitization.
"""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.services.auth_services import user_register, user_generate_tokens
from apps.problems.models import Category, Problem, TestCase
from apps.submissions.models import Submission, SubmissionStatus
from apps.submissions.tasks import evaluate_submission_task


@pytest.fixture
def student_user(db):
    return user_register(
        username="codestudent",
        email="student@skillforge.test",
        password="StudentPassword123!",
        display_name="Code Student"
    )


@pytest.fixture
def other_student_user(db):
    return user_register(
        username="otherstudent",
        email="other@skillforge.test",
        password="StudentPassword123!",
        display_name="Other Student"
    )


@pytest.fixture
def admin_user(db):
    admin = user_register(
        username="evaladmin",
        email="evaladmin@skillforge.test",
        password="AdminPassword123!",
        display_name="Eval Admin"
    )
    admin.is_staff = True
    admin.save(update_fields=['is_staff'])
    return admin


@pytest.fixture
def student_client(student_user):
    client = APIClient()
    access, _ = user_generate_tokens(user=student_user)
    client.cookies['access_token'] = access
    return client


@pytest.fixture
def other_student_client(other_student_user):
    client = APIClient()
    access, _ = user_generate_tokens(user=other_student_user)
    client.cookies['access_token'] = access
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    access, _ = user_generate_tokens(user=admin_user)
    client.cookies['access_token'] = access
    return client


@pytest.fixture
def coding_problem(db):
    cat = Category.objects.create(name="Algorithms", slug="algorithms")
    prob = Problem.objects.create(
        title="Array Multiplier",
        slug="array-multiplier",
        description="Multiply array elements.",
        difficulty="easy",
        challenge_level=1,
        category=cat,
        xp_reward=50,
        is_published=True
    )
    TestCase.objects.create(
        problem=prob,
        input_data="2\n2 3",
        expected_output="6",
        is_sample=True,
        order=1
    )
    TestCase.objects.create(
        problem=prob,
        input_data="3\n1 2 4",
        expected_output="8",
        is_sample=False,
        order=2
    )
    return prob


@pytest.mark.django_db
class TestSubmissionsAPI:
    def test_submit_unauthenticated_fails(self, coding_problem):
        client = APIClient()
        url = reverse('submission-list-create')
        payload = {
            "problem_id": coding_problem.id,
            "source_code": "int main() { return 0; }",
            "language": "cpp"
        }
        response = client.post(url, data=payload, format='json')
        assert response.status_code == 401

    def test_submit_code_creates_pending_submission(self, student_client, coding_problem):
        url = reverse('submission-list-create')
        payload = {
            "problem_id": coding_problem.id,
            "source_code": "#include <iostream>\nusing namespace std;\nint main() { return 0; }",
            "language": "cpp",
            "is_sample_run": False
        }
        response = student_client.post(url, data=payload, format='json')
        assert response.status_code == 201
        assert response.data['status'] == SubmissionStatus.PENDING
        assert response.data['problem_id'] == coding_problem.id

    def test_synchronous_evaluation_execution(self, student_user, coding_problem):
        submission = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="#include <iostream>\nusing namespace std;\nint main() {\n    cout << 6 << endl;\n    return 0;\n}",
            status=SubmissionStatus.PENDING
        )
        # Directly run the Celery task synchronously
        evaluate_submission_task(submission.id)

        submission.refresh_from_db()
        assert submission.status == SubmissionStatus.ACCEPTED
        assert submission.passed_test_cases_count == 2
        assert submission.total_test_cases_count == 2
        assert submission.execution_time is not None

    def test_sample_run_only_evaluates_sample_cases(self, student_user, coding_problem):
        submission = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="#include <iostream>\nint main() { return 0; }",
            is_sample_run=True,
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(submission.id)

        submission.refresh_from_db()
        assert submission.total_test_cases_count == 1  # Only the 1 sample case
        assert submission.passed_test_cases_count == 1

    def test_hidden_test_cases_sanitization_for_student(self, student_client, student_user, coding_problem):
        submission = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="#include <iostream>\nint main() { return 0; }",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(submission.id)

        url = reverse('submission-detail', kwargs={'submission_id': submission.id})
        response = student_client.get(url)
        assert response.status_code == 200

        results = response.data['results']
        assert len(results) == 2

        # Sample case has visible input/expected
        sample_res = [r for r in results if r['is_sample']][0]
        assert sample_res['input_data'] == "2\n2 3"
        assert sample_res['expected_output'] == "6"

        # Hidden case MUST be masked
        hidden_res = [r for r in results if not r['is_sample']][0]
        assert hidden_res['input_data'] == "[Hidden Test Case]"
        assert hidden_res['expected_output'] == "[Hidden Test Case]"

    def test_admin_can_view_unmasked_hidden_cases(self, admin_client, student_user, coding_problem):
        submission = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="#include <iostream>\nint main() { return 0; }",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(submission.id)

        url = reverse('submission-detail', kwargs={'submission_id': submission.id})
        response = admin_client.get(url)
        assert response.status_code == 200

        results = response.data['results']
        hidden_res = [r for r in results if not r['is_sample']][0]
        assert hidden_res['input_data'] == "3\n1 2 4"
        assert hidden_res['expected_output'] == "8"

    def test_submission_ownership_isolation(self, other_student_client, student_user, coding_problem):
        submission = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="#include <iostream>\nint main() { return 0; }",
            status=SubmissionStatus.ACCEPTED
        )
        url = reverse('submission-detail', kwargs={'submission_id': submission.id})
        response = other_student_client.get(url)
        # Should return 404 Not Found to unauthorized student
        assert response.status_code == 404

    def test_award_xp_anti_farming(self, student_user, coding_problem):
        profile = student_user.profile
        initial_xp = profile.total_xp
        initial_solved = profile.problems_solved_count

        # First accepted solve
        sub1 = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="#include <iostream>\nint main() { return 0; }",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub1.id)

        profile.refresh_from_db()
        assert profile.total_xp == initial_xp + coding_problem.xp_reward
        assert profile.problems_solved_count == initial_solved + 1

        # Second accepted solve on the SAME problem
        sub2 = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="#include <iostream>\nint main() { return 0; }",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub2.id)

        profile.refresh_from_db()
        # XP and solved count must NOT increase a second time!
        assert profile.total_xp == initial_xp + coding_problem.xp_reward
        assert profile.problems_solved_count == initial_solved + 1

    def test_compilation_error_handling(self, student_user, coding_problem):
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="this_is_syntax_error int foo;",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)

        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.COMPILATION_ERROR
        assert "error" in sub.compile_output

    def test_time_limit_exceeded_handling(self, student_user, coding_problem):
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="#include <iostream>\nint main() { while(true) {} return 0; }",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)

        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.TIME_LIMIT_EXCEEDED

    def test_python_submission_evaluation(self, student_user, coding_problem):
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='python',
            source_code="import sys\ndef solve():\n    print(1)\nsolve()",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)
        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.ACCEPTED
        assert sub.language == 'python'

    def test_javascript_submission_evaluation(self, student_user, coding_problem):
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='javascript',
            source_code="const fs = require('fs');\nfunction solve() { console.log(1); }\nsolve();",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)
        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.ACCEPTED
        assert sub.language == 'javascript'

