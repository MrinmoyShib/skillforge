"""
Public API views for browsing and retrieving coding problems.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from ..serializers.input import ProblemFilterInputSerializer
from ..serializers.output import (
    ProblemListOutputSerializer,
    ProblemDetailOutputSerializer,
    CategoryOutputSerializer,
    TagOutputSerializer,
)
from ..selectors.problem_selectors import (
    problem_list,
    problem_get_by_slug,
    category_list,
    tag_list,
)
from apps.core.pagination import StandardPagination


class ProblemListAPI(APIView):
    """
    Catalog of published coding problems with search and filter capabilities.
    """
    permission_classes = [AllowAny]
    pagination_class = StandardPagination

    @extend_schema(
        summary="List Problems",
        description="Returns paginated list of published coding problems filtered by difficulty, category, level, or search term.",
        parameters=[ProblemFilterInputSerializer],
        responses={200: ProblemListOutputSerializer(many=True)}
    )
    def get(self, request):
        filter_serializer = ProblemFilterInputSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        is_admin = bool(request.user and request.user.is_authenticated and request.user.is_staff)
        problems = problem_list(filters=filter_serializer.validated_data, is_admin=is_admin)

        paginator = self.pagination_class()
        paginated_problems = paginator.paginate_queryset(problems, request)
        serializer = ProblemListOutputSerializer(paginated_problems, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProblemDetailAPI(APIView):
    """
    Detailed problem statement and public sample test cases.
    Hidden evaluation test cases are strictly excluded.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Problem Detail",
        description="Retrieves a single problem by slug, including its description, constraints, and public sample test cases.",
        responses={200: ProblemDetailOutputSerializer}
    )
    def get(self, request, slug):
        is_admin = bool(request.user and request.user.is_authenticated and request.user.is_staff)
        problem = problem_get_by_slug(slug=slug, is_admin=is_admin)

        if not problem:
            raise NotFound("Problem not found.")

        serializer = ProblemDetailOutputSerializer(problem)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListAPI(APIView):
    """
    Lists problem categories with published problem counts.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List Categories",
        description="Returns all problem categories with their active problem count.",
        responses={200: CategoryOutputSerializer(many=True)}
    )
    def get(self, request):
        categories = category_list()
        serializer = CategoryOutputSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagListAPI(APIView):
    """
    Lists all problem tags.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List Tags",
        description="Returns all taxonomy tags.",
        responses={200: TagOutputSerializer(many=True)}
    )
    def get(self, request):
        tags = tag_list()
        serializer = TagOutputSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

