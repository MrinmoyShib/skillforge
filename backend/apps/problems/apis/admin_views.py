"""
Admin API views for managing Problems and Test Cases.
Restricted exclusively to staff administrators.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from apps.accounts.permissions import IsAdminRole
from apps.core.pagination import StandardPagination
from ..models import TestCase
from ..serializers.input import (
    ProblemCreateInputSerializer,
    ProblemUpdateInputSerializer,
    TestCaseCreateInputSerializer,
    TestCaseUpdateInputSerializer,
)
from ..serializers.output import (
    ProblemListOutputSerializer,
    AdminProblemDetailOutputSerializer,
    AdminTestCaseOutputSerializer,
)
from ..selectors.problem_selectors import (
    problem_list,
    problem_get_by_id,
    test_cases_for_problem,
)
from ..services.problem_services import (
    problem_create,
    problem_update,
    problem_delete,
    test_case_create,
    test_case_update,
    test_case_delete,
)


class AdminProblemListCreateAPI(APIView):
    permission_classes = [IsAdminRole]
    pagination_class = StandardPagination

    @extend_schema(
        summary="Admin List Problems",
        description="Returns all problems including draft/unpublished challenges.",
        responses={200: ProblemListOutputSerializer(many=True)}
    )
    def get(self, request):
        problems = problem_list(is_admin=True)
        paginator = self.pagination_class()
        paginated_problems = paginator.paginate_queryset(problems, request)
        serializer = ProblemListOutputSerializer(paginated_problems, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Admin Create Problem",
        description="Creates a new coding problem.",
        request=ProblemCreateInputSerializer,
        responses={201: AdminProblemDetailOutputSerializer}
    )
    def post(self, request):
        serializer = ProblemCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        problem = problem_create(**serializer.validated_data)
        detailed_problem = problem_get_by_id(problem_id=problem.id)
        return Response(AdminProblemDetailOutputSerializer(detailed_problem).data, status=status.HTTP_201_CREATED)


class AdminProblemDetailAPI(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        summary="Admin Problem Detail",
        description="Retrieves a problem including all private/hidden evaluation test cases.",
        responses={200: AdminProblemDetailOutputSerializer}
    )
    def get(self, request, problem_id):
        problem = problem_get_by_id(problem_id=problem_id)
        if not problem:
            raise NotFound("Problem not found.")
        return Response(AdminProblemDetailOutputSerializer(problem).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Admin Update Problem",
        description="Updates fields of an existing problem.",
        request=ProblemUpdateInputSerializer,
        responses={200: AdminProblemDetailOutputSerializer}
    )
    def patch(self, request, problem_id):
        problem = problem_get_by_id(problem_id=problem_id)
        if not problem:
            raise NotFound("Problem not found.")

        serializer = ProblemUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_problem = problem_update(problem=problem, **serializer.validated_data)
        detailed_problem = problem_get_by_id(problem_id=updated_problem.id)
        return Response(AdminProblemDetailOutputSerializer(detailed_problem).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Admin Delete Problem",
        description="Permanently deletes a problem and its test cases.",
        responses={204: None}
    )
    def delete(self, request, problem_id):
        problem = problem_get_by_id(problem_id=problem_id)
        if not problem:
            raise NotFound("Problem not found.")
        problem_delete(problem=problem)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminTestCaseListCreateAPI(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        summary="Admin List Test Cases",
        description="Lists all test cases (sample and hidden) for a specific problem.",
        responses={200: AdminTestCaseOutputSerializer(many=True)}
    )
    def get(self, request, problem_id):
        problem = problem_get_by_id(problem_id=problem_id)
        if not problem:
            raise NotFound("Problem not found.")
        cases = test_cases_for_problem(problem_id=problem.id)
        return Response(AdminTestCaseOutputSerializer(cases, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Admin Create Test Case",
        description="Creates a new test case for a problem.",
        request=TestCaseCreateInputSerializer,
        responses={201: AdminTestCaseOutputSerializer}
    )
    def post(self, request, problem_id):
        problem = problem_get_by_id(problem_id=problem_id)
        if not problem:
            raise NotFound("Problem not found.")

        serializer = TestCaseCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        case = test_case_create(problem=problem, **serializer.validated_data)
        return Response(AdminTestCaseOutputSerializer(case).data, status=status.HTTP_201_CREATED)


class AdminTestCaseDetailAPI(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        summary="Admin Update Test Case",
        description="Updates an existing test case.",
        request=TestCaseUpdateInputSerializer,
        responses={200: AdminTestCaseOutputSerializer}
    )
    def patch(self, request, test_case_id):
        case = TestCase.objects.filter(id=test_case_id).first()
        if not case:
            raise NotFound("Test case not found.")

        serializer = TestCaseUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_case = test_case_update(test_case=case, **serializer.validated_data)
        return Response(AdminTestCaseOutputSerializer(updated_case).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Admin Delete Test Case",
        description="Deletes a test case.",
        responses={204: None}
    )
    def delete(self, request, test_case_id):
        case = TestCase.objects.filter(id=test_case_id).first()
        if not case:
            raise NotFound("Test case not found.")
        test_case_delete(test_case=case)
        return Response(status=status.HTTP_204_NO_CONTENT)
