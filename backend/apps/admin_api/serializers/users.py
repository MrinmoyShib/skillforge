"""
Serializers for Admin User Directory & Student Intelligence.
"""
from rest_framework import serializers
from apps.accounts.models import User, UserProfile
from apps.progress.models import UserProgress, ActivityLog
from apps.projects.models import UserProjectProgress
from apps.submissions.models import Submission


class AdminUserListSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='profile.display_name', read_only=True)
    avatar_url = serializers.CharField(source='profile.avatar_url', read_only=True)
    current_level = serializers.IntegerField(source='profile.current_level', read_only=True)
    level_title = serializers.SerializerMethodField()
    total_xp = serializers.IntegerField(source='profile.total_xp', read_only=True)
    problems_solved_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'display_name',
            'avatar_url',
            'is_staff',
            'is_active',
            'current_level',
            'level_title',
            'total_xp',
            'problems_solved_count',
            'date_joined',
            'last_login',
        ]

    def get_level_title(self, obj):
        from apps.progress.services.leveling import calculate_level
        total_xp = getattr(obj.profile, 'total_xp', 0) if hasattr(obj, 'profile') else 0
        return calculate_level(total_xp)['title']


class AdminUserDetailSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='profile.display_name', read_only=True)
    avatar_url = serializers.CharField(source='profile.avatar_url', read_only=True)
    phone_number = serializers.CharField(source='profile.phone_number', read_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)
    github_url = serializers.CharField(source='profile.github_url', read_only=True)
    linkedin_url = serializers.CharField(source='profile.linkedin_url', read_only=True)
    twitter_url = serializers.CharField(source='profile.twitter_url', read_only=True)
    website_url = serializers.CharField(source='profile.website_url', read_only=True)
    current_level = serializers.IntegerField(source='profile.current_level', read_only=True)
    level_title = serializers.SerializerMethodField()
    total_xp = serializers.IntegerField(source='profile.total_xp', read_only=True)
    streak_days = serializers.IntegerField(source='profile.current_streak_days', read_only=True)
    
    track_breakdown = serializers.SerializerMethodField()
    enrolled_projects = serializers.SerializerMethodField()
    recent_submissions = serializers.SerializerMethodField()
    recent_activity = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'display_name',
            'avatar_url',
            'phone_number',
            'bio',
            'location',
            'github_url',
            'linkedin_url',
            'twitter_url',
            'website_url',
            'is_staff',
            'is_active',
            'current_level',
            'level_title',
            'total_xp',
            'streak_days',
            'date_joined',
            'last_login',
            'track_breakdown',
            'enrolled_projects',
            'recent_submissions',
            'recent_activity',
        ]

    def get_level_title(self, obj):
        from apps.progress.services.leveling import calculate_level
        total_xp = getattr(obj.profile, 'total_xp', 0) if hasattr(obj, 'profile') else 0
        return calculate_level(total_xp)['title']

    def get_track_breakdown(self, obj):
        # Count solved problems per language track
        from apps.problems.models import Problem
        tracks = ['python', 'javascript', 'cpp']
        breakdown = {}
        for track in tracks:
            solved_count = UserProgress.objects.filter(
                user=obj,
                solved=True,
                problem__language=track
            ).count()
            total_count = Problem.objects.filter(language=track, is_published=True).count()
            breakdown[track] = {
                "solved": solved_count,
                "total": total_count,
                "remaining": max(0, total_count - solved_count),
            }
        return breakdown

    def get_enrolled_projects(self, obj):
        records = UserProjectProgress.objects.filter(user=obj).select_related('project').prefetch_related('completed_milestones')
        data = []
        for r in records:
            total_milestones = r.project.milestones.count()
            completed_count = r.completed_milestones.count()
            data.append({
                "project_id": r.project.id,
                "title": r.project.title,
                "slug": r.project.slug,
                "language": r.project.language,
                "status": r.status,
                "completed_milestones_count": completed_count,
                "total_milestones_count": total_milestones,
                "last_active_at": r.last_active_at,
            })
        return data

    def get_recent_submissions(self, obj):
        subs = Submission.objects.filter(user=obj).select_related('problem').order_by('-created_at')[:10]
        return [
            {
                "id": s.id,
                "problem_id": s.problem.id,
                "problem_title": s.problem.title,
                "problem_slug": s.problem.slug,
                "language": s.language,
                "status": s.status,
                "execution_time": s.execution_time,
                "memory_usage": s.memory_usage,
                "created_at": s.created_at,
            }
            for s in subs
        ]

    def get_recent_activity(self, obj):
        logs = ActivityLog.objects.filter(user=obj).order_by('-created_at')[:10]
        return [
            {
                "id": log.id,
                "activity_type": log.activity_type,
                "description": log.description,
                "xp_gained": log.metadata.get('xp_delta', log.metadata.get('xp_gained', 0)),
                "created_at": log.created_at,
            }
            for log in logs
        ]


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_staff', 'is_active']


class AdminAdjustXPInputSerializer(serializers.Serializer):
    xp_delta = serializers.IntegerField(required=True, help_text="Amount of XP to add or subtract")
    reason = serializers.CharField(max_length=255, required=True, help_text="Audit reason for the XP adjustment")
