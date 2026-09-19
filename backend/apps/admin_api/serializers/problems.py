"""
Serializers for Admin Problem Studio & Test Case Management.
"""
from rest_framework import serializers
from apps.problems.models import Problem, TestCase, Category, Tag


class AdminTestCaseSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    input_data = serializers.CharField(allow_blank=True, default="")
    expected_output = serializers.CharField(allow_blank=True, default="")
    is_sample = serializers.BooleanField(default=False)
    order = serializers.IntegerField(default=1)


class AdminProblemListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    test_cases_count = serializers.IntegerField(read_only=True)
    solves_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'slug',
            'language',
            'difficulty',
            'challenge_level',
            'xp_reward',
            'is_published',
            'category_name',
            'tags',
            'test_cases_count',
            'solves_count',
            'created_at',
        ]


class AdminProblemDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    test_cases = AdminTestCaseSerializer(many=True, read_only=True)
    solves_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'difficulty',
            'challenge_level',
            'category_id',
            'category_name',
            'tags',
            'xp_reward',
            'constraints',
            'input_format',
            'output_format',
            'examples',
            'starter_code',
            'language',
            'time_limit_seconds',
            'memory_limit_kb',
            'is_published',
            'test_cases',
            'solves_count',
            'created_at',
            'updated_at',
        ]


class AdminProblemCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_blank=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    category_slug = serializers.CharField(required=False, write_only=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    test_cases = AdminTestCaseSerializer(many=True, required=False)

    class Meta:
        model = Problem
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'difficulty',
            'challenge_level',
            'category',
            'category_slug',
            'tags',
            'tag_ids',
            'xp_reward',
            'constraints',
            'input_format',
            'output_format',
            'examples',
            'starter_code',
            'language',
            'time_limit_seconds',
            'memory_limit_kb',
            'is_published',
            'test_cases',
        ]
        read_only_fields = ['id']

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = dict(data)
            if 'category_id' in data and 'category' not in data:
                data['category'] = data.pop('category_id')
        return super().to_internal_value(data)

    def validate(self, attrs):
        category = attrs.get('category')
        category_slug = attrs.pop('category_slug', None)

        if not attrs.get('slug') and attrs.get('title'):
            from django.utils.text import slugify
            base_slug = slugify(attrs['title'])
            slug = base_slug
            counter = 1
            qs = Problem.objects.all()
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            while qs.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            attrs['slug'] = slug

        if not category and category_slug:
            cat, _ = Category.objects.get_or_create(
                slug=category_slug,
                defaults={'name': category_slug.replace('-', ' ').title()}
            )
            attrs['category'] = cat
        elif not category and not self.instance:
            first_cat = Category.objects.first()
            if not first_cat:
                first_cat = Category.objects.create(name='General', slug='general')
            attrs['category'] = first_cat

        return attrs

    def create(self, validated_data):
        test_cases_data = validated_data.pop('test_cases', [])
        tags_data = validated_data.pop('tags', [])
        tag_ids_data = validated_data.pop('tag_ids', [])

        problem = Problem.objects.create(**validated_data)

        if tags_data:
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name, defaults={'slug': tag_name.lower().replace(' ', '-')})
                problem.tags.add(tag)

        if tag_ids_data:
            problem.tags.add(*tag_ids_data)

        for tc_data in test_cases_data:
            TestCase.objects.create(problem=problem, **tc_data)

        return problem

    def update(self, instance, validated_data):
        test_cases_data = validated_data.pop('test_cases', None)
        tags_data = validated_data.pop('tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name, defaults={'slug': tag_name.lower().replace(' ', '-')})
                instance.tags.add(tag)

        if test_cases_data is not None:
            # Update or create test cases
            existing_tc_ids = set(instance.test_cases.values_list('id', flat=True))
            incoming_tc_ids = {tc['id'] for tc in test_cases_data if 'id' in tc}

            # Delete test cases not in incoming list
            to_delete = existing_tc_ids - incoming_tc_ids
            if to_delete:
                TestCase.objects.filter(id__in=to_delete).delete()

            for idx, tc in enumerate(test_cases_data):
                tc_id = tc.get('id')
                if tc_id and tc_id in existing_tc_ids:
                    TestCase.objects.filter(id=tc_id).update(
                        input_data=tc.get('input_data', ''),
                        expected_output=tc.get('expected_output', ''),
                        is_sample=tc.get('is_sample', False),
                        order=tc.get('order', idx + 1)
                    )
                else:
                    TestCase.objects.create(
                        problem=instance,
                        input_data=tc.get('input_data', ''),
                        expected_output=tc.get('expected_output', ''),
                        is_sample=tc.get('is_sample', False),
                        order=tc.get('order', idx + 1)
                    )

        return instance


class AdminVerifySolutionInputSerializer(serializers.Serializer):
    source_code = serializers.CharField(required=True)
    language = serializers.CharField(required=False)


class TestCaseVerificationResultSerializer(serializers.Serializer):
    test_case_id = serializers.IntegerField(allow_null=True)
    order = serializers.IntegerField()
    is_sample = serializers.BooleanField()
    status = serializers.CharField()
    execution_time = serializers.FloatField(allow_null=True)
    memory_usage = serializers.IntegerField(allow_null=True)
    stdout = serializers.CharField(allow_blank=True)
    stderr = serializers.CharField(allow_blank=True)
    expected_output = serializers.CharField(allow_blank=True)


class AdminVerifySolutionOutputSerializer(serializers.Serializer):
    all_passed = serializers.BooleanField()
    passed_count = serializers.IntegerField()
    total_count = serializers.IntegerField()
    results = TestCaseVerificationResultSerializer(many=True)
    compile_output = serializers.CharField(allow_blank=True, default="")
    error_message = serializers.CharField(allow_blank=True, default="")
