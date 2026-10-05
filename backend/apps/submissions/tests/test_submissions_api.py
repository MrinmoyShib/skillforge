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
        display_name="Code Student",
        is_active=True
    )


@pytest.fixture
def other_student_user(db):
    return user_register(
        username="otherstudent",
        email="other@skillforge.test",
        password="StudentPassword123!",
        display_name="Other Student",
        is_active=True
    )


@pytest.fixture
def admin_user(db):
    admin = user_register(
        username="evaladmin",
        email="evaladmin@skillforge.test",
        password="AdminPassword123!",
        display_name="Eval Admin",
        is_active=True
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
        real_cpp_solution = (
            "#include <iostream>\n"
            "using namespace std;\n"
            "int main() {\n"
            "    int n;\n"
            "    if (cin >> n) {\n"
            "        long long p = 1;\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            long long x;\n"
            "            cin >> x;\n"
            "            p *= x;\n"
            "        }\n"
            "        cout << p << endl;\n"
            "    }\n"
            "    return 0;\n"
            "}\n"
        )
        submission = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code=real_cpp_solution,
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
            source_code="// # mock_accepted\n#include <iostream>\nint main() { return 0; }",
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
            source_code="// # mock_accepted\n#include <iostream>\nint main() { return 0; }",
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
            source_code="// # mock_accepted\n#include <iostream>\nint main() { return 0; }",
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
            source_code="// # mock_accepted\n#include <iostream>\nint main() { return 0; }",
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
            source_code="// # mock_accepted\n#include <iostream>\nint main() { return 0; }",
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
        real_solution = (
            "import sys\n"
            "from functools import reduce\n"
            "import operator\n"
            "lines = sys.stdin.read().strip().splitlines()\n"
            "if lines:\n"
            "    arr = list(map(int, lines[1].split()))\n"
            "    print(reduce(operator.mul, arr, 1))\n"
        )
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='python',
            source_code=real_solution,
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)
        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.ACCEPTED
        assert sub.language == 'python'
        assert sub.passed_test_cases_count == 2

    def test_python_submission_random_code_fails_evaluation(self, student_user, coding_problem):
        """
        Verify BUG-028 fix: random or unsolved Python code must receive WRONG_ANSWER
        and NOT be falsely marked ACCEPTED.
        """
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='python',
            source_code="x = 42\nprint('random code')",
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)
        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.WRONG_ANSWER
        assert sub.passed_test_cases_count == 0

    def test_javascript_submission_evaluation(self, student_user, coding_problem):
        js_solution = (
            "const fs = require('fs');\n"
            "const tokens = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/);\n"
            "if (tokens.length > 1) {\n"
            "    const n = parseInt(tokens[0], 10);\n"
            "    let prod = 1;\n"
            "    for (let i = 1; i <= n; i++) {\n"
            "        prod *= parseInt(tokens[i], 10);\n"
            "    }\n"
            "    console.log(prod);\n"
            "}\n"
        )
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='javascript',
            source_code=js_solution,
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)
        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.ACCEPTED
        assert sub.language == 'javascript'
        assert sub.passed_test_cases_count == 2

    def test_cpp_submission_unsolved_code_fails_evaluation(self, student_user, coding_problem):
        """
        Verify empty starter / unsolved C++ boilerplate fails evaluation
        with WRONG_ANSWER and 0 passed cases, and awards NO XP.
        """
        initial_xp = student_user.profile.total_xp
        unsolved_code = (
            "#include <iostream>\n"
            "#include <vector>\n"
            "using namespace std;\n\n"
            "int main() {\n"
            "    // Write your solution here\n"
            "    return 0;\n"
            "}\n"
        )
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code=unsolved_code,
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)
        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.WRONG_ANSWER
        assert sub.passed_test_cases_count == 0
        student_user.profile.refresh_from_db()
        assert student_user.profile.total_xp == initial_xp

    def test_javascript_submission_unsolved_code_fails_evaluation(self, student_user, coding_problem):
        """
        Verify empty starter / unsolved JavaScript boilerplate fails evaluation
        with WRONG_ANSWER and 0 passed cases.
        """
        unsolved_code = "function solve() {}\nsolve();"
        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='javascript',
            source_code=unsolved_code,
            status=SubmissionStatus.PENDING
        )
        evaluate_submission_task(sub.id)
        sub.refresh_from_db()
        assert sub.status == SubmissionStatus.WRONG_ANSWER
        assert sub.passed_test_cases_count == 0

    def test_submission_rejects_unsupported_language(self, student_client, coding_problem):
        """
        Verify BUG-044 fix: invalid or unsupported language choices are rejected by the serializer.
        """
        url = reverse('submission-list-create')
        payload = {
            "problem_id": coding_problem.id,
            "source_code": "fn main() { println!(\"hello\"); }",
            "language": "rust",
            "is_sample_run": False
        }
        response = student_client.post(url, data=payload, format='json')
        assert response.status_code == 400
        errors = response.data.get("errors", response.data)
        assert "language" in errors

    def test_submission_rejects_mismatched_problem_language(self, student_client, coding_problem):
        """
        Verify BUG-044 fix: submitting a solution in a language that does not match
        the problem's target track language is rejected.
        """
        url = reverse('submission-list-create')
        payload = {
            "problem_id": coding_problem.id,  # problem.language is 'cpp'
            "source_code": "def solve(): return 42",
            "language": "python",
            "is_sample_run": False
        }
        response = student_client.post(url, data=payload, format='json')
        assert response.status_code == 400
        errors = response.data.get("errors", response.data)
        assert "language" in errors
        assert "designed for" in str(errors["language"])

    def test_submission_task_handles_transient_failure_and_retries(self, student_user, coding_problem, monkeypatch):
        """
        Verify BUG-013 fix: evaluate_submission_task invokes self.retry when transient exceptions occur.
        """
        from unittest.mock import MagicMock
        from apps.submissions.engine.base import AbstractExecutionEngine, ExecutionResult

        sub = Submission.objects.create(
            user=student_user,
            problem=coding_problem,
            language='cpp',
            source_code="int main() { return 0; }",
            status=SubmissionStatus.PENDING
        )

        retry_called = []

        # Mock evaluate_submission_task.retry to record invocation
        def fake_retry(*args, **kwargs):
            retry_called.append(True)
            raise evaluate_submission_task.MaxRetriesExceededError("Max retries exceeded")

        monkeypatch.setattr(evaluate_submission_task, "retry", fake_retry)

        # Mock engine to raise transient connection error
        class BrokenEngine(AbstractExecutionEngine):
            def is_available(self):
                return True

            def execute(self, **kwargs):
                raise ConnectionResetError("Docker daemon socket timed out")

        monkeypatch.setattr("apps.submissions.tasks.get_execution_engine", lambda: BrokenEngine())

        evaluate_submission_task(sub.id)
        sub.refresh_from_db()
        assert retry_called == [True]
        assert sub.status == SubmissionStatus.INTERNAL_ERROR
        assert "Docker daemon socket timed out" in sub.error_message

