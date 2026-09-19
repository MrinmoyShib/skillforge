"""
Serializers for Admin Guided Projects & Milestones Management.
"""
from rest_framework import serializers
from apps.projects.models import Project, ProjectMilestone


class AdminProjectMilestoneSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    order = serializers.IntegerField(default=1)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, default="")
    starter_code = serializers.CharField(allow_blank=True, default="")
    test_harness_code = serializers.CharField(allow_blank=True, default="")
    hints = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    xp_reward = serializers.IntegerField(default=50)


class AdminProjectListSerializer(serializers.ModelSerializer):
    milestones_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'language',
            'difficulty',
            'challenge_level',
            'short_description',
            'technologies',
            'xp_reward',
            'estimated_minutes',
            'is_published',
            'order',
            'milestones_count',
            'created_at',
        ]


class AdminProjectDetailSerializer(serializers.ModelSerializer):
    milestones = AdminProjectMilestoneSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'language',
            'difficulty',
            'challenge_level',
            'short_description',
            'description',
            'technologies',
            'starter_files',
            'xp_reward',
            'estimated_minutes',
            'is_published',
            'order',
            'milestones',
            'created_at',
            'updated_at',
        ]


class AdminProjectCreateUpdateSerializer(serializers.ModelSerializer):
    milestones = AdminProjectMilestoneSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'language',
            'difficulty',
            'challenge_level',
            'short_description',
            'description',
            'technologies',
            'starter_files',
            'xp_reward',
            'estimated_minutes',
            'is_published',
            'order',
            'milestones',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        milestones_data = validated_data.pop('milestones', [])
        project = Project.objects.create(**validated_data)

        for m_data in milestones_data:
            ProjectMilestone.objects.create(project=project, **m_data)

        return project

    def update(self, instance, validated_data):
        milestones_data = validated_data.pop('milestones', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if milestones_data is not None:
            existing_m_ids = set(instance.milestones.values_list('id', flat=True))
            incoming_m_ids = {m['id'] for m in milestones_data if 'id' in m}

            to_delete = existing_m_ids - incoming_m_ids
            if to_delete:
                ProjectMilestone.objects.filter(id__in=to_delete).delete()

            for idx, m in enumerate(milestones_data):
                m_id = m.get('id')
                if m_id and m_id in existing_m_ids:
                    ProjectMilestone.objects.filter(id=m_id).update(
                        order=m.get('order', idx + 1),
                        title=m.get('title', ''),
                        description=m.get('description', ''),
                        starter_code=m.get('starter_code', ''),
                        test_harness_code=m.get('test_harness_code', ''),
                        hints=m.get('hints', []),
                        xp_reward=m.get('xp_reward', 50),
                    )
                else:
                    ProjectMilestone.objects.create(
                        project=instance,
                        order=m.get('order', idx + 1),
                        title=m.get('title', ''),
                        description=m.get('description', ''),
                        starter_code=m.get('starter_code', ''),
                        test_harness_code=m.get('test_harness_code', ''),
                        hints=m.get('hints', []),
                        xp_reward=m.get('xp_reward', 50),
                    )

        return instance
