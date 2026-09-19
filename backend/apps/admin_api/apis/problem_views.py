"""
Admin Problem Studio ViewSet with Test Case Manager and Sandbox Verification.
"""
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.problems.models import Problem, TestCase
from apps.submissions.engine import get_execution_engine
from apps.submissions.models import SubmissionStatus
from ..serializers.problems import (
    AdminProblemListSerializer,
    AdminProblemDetailSerializer,
    AdminProblemCreateUpdateSerializer,
    AdminVerifySolutionInputSerializer,
    AdminVerifySolutionOutputSerializer,
)


class AdminProblemViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for Problem management in Admin Studio.
    Includes in-studio sandbox verification runner.
    """
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = Problem.objects.select_related('category').prefetch_related('tags', 'test_cases').annotate(
            test_cases_count=Count('test_cases', distinct=True),
            solves_count=Count('progress_records', filter=Q(progress_records__solved=True), distinct=True)
        )

        # Filters
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(slug__icontains=search) | Q(description__icontains=search))

        language = self.request.query_params.get('language')
        if language:
            qs = qs.filter(language=language)

        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            qs = qs.filter(difficulty=difficulty)

        challenge_level = self.request.query_params.get('challenge_level')
        if challenge_level:
            qs = qs.filter(challenge_level=challenge_level)

        is_published = self.request.query_params.get('is_published')
        if is_published is not None:
            qs = qs.filter(is_published=is_published.lower() in ('true', '1'))

        return qs.order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminProblemListSerializer
        elif self.action == 'retrieve':
            return AdminProblemDetailSerializer
        return AdminProblemCreateUpdateSerializer

    @action(detail=True, methods=['post'], url_path='verify')
    def verify_solution(self, request, pk=None):
        """
        Runs an author's solution against all test cases for this problem inside the sandbox.
        Allows problem authors to test reference solutions before publishing.
        """
        problem = self.get_object()
        serializer = AdminVerifySolutionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_code = serializer.validated_data['source_code']
        language = serializer.validated_data.get('language') or problem.language

        test_cases = list(problem.test_cases.all().order_by('order', 'id'))
        if not test_cases:
            return Response(
                {"detail": "This problem has no test cases defined yet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        engine = get_execution_engine()
        results = []
        passed_count = 0
        compile_output = ""
        error_message = ""

        for tc in test_cases:
            res = engine.execute(
                source_code=source_code,
                language=language,
                stdin=tc.input_data,
                expected_output=tc.expected_output,
                time_limit=problem.time_limit_seconds,
                memory_limit=problem.memory_limit_kb
            )

            if res.compile_output and not compile_output:
                compile_output = res.compile_output
            if res.error_message and not error_message:
                error_message = res.error_message

            is_passed = (res.status == SubmissionStatus.ACCEPTED)
            if is_passed:
                passed_count += 1

            results.append({
                "test_case_id": tc.id,
                "order": tc.order,
                "is_sample": tc.is_sample,
                "status": res.status,
                "execution_time": res.execution_time,
                "memory_usage": res.memory_usage,
                "stdout": res.stdout or "",
                "stderr": res.stderr or "",
                "expected_output": tc.expected_output,
            })

            if res.status == SubmissionStatus.COMPILATION_ERROR:
                break

        data = {
            "all_passed": (passed_count == len(test_cases)),
            "passed_count": passed_count,
            "total_count": len(test_cases),
            "results": results,
            "compile_output": compile_output,
            "error_message": error_message,
        }
        output_serializer = AdminVerifySolutionOutputSerializer(data)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
