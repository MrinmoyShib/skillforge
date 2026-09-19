"""
Query selectors for Guided Projects and User Project Progress.
"""
from typing import Optional, Dict, Any, List
from django.db.models import Q
from ..models import Project, UserProjectProgress


def project_list(*, user=None, filters: Optional[Dict[str, Any]] = None) -> List[dict]:
    """
    Returns filtered projects annotated with milestone counts and user progress.
    """
    qs = Project.objects.filter(is_published=True).prefetch_related('milestones')

    if filters:
        if filters.get('language'):
            qs = qs.filter(language=filters['language'])
        if filters.get('difficulty'):
            qs = qs.filter(difficulty=filters['difficulty'])
        if filters.get('search'):
            term = filters['search'].strip()
            qs = qs.filter(Q(title__icontains=term) | Q(short_description__icontains=term) | Q(description__icontains=term))

    user_progress_map = {}
    if user and user.is_authenticated:
        progress_records = UserProjectProgress.objects.filter(user=user, project__in=qs)
        user_progress_map = {p.project_id: p for p in progress_records}

    results = []
    status_filter = filters.get('status') if filters else None

    for p in qs:
        up = user_progress_map.get(p.id)
        u_status = up.status if up else 'NOT_STARTED'
        completed_count = len(up.completed_milestones) if up else 0

        if status_filter and u_status != status_filter:
            continue

        results.append({
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "language": p.language,
            "difficulty": p.difficulty,
            "challenge_level": p.challenge_level,
            "short_description": p.short_description,
            "technologies": p.technologies or [],
            "xp_reward": p.xp_reward,
            "estimated_minutes": p.estimated_minutes,
            "milestones_count": p.milestones.count(),
            "user_status": u_status,
            "completed_milestones_count": completed_count,
        })

    return results


def project_get_by_slug(*, slug: str, user=None) -> Optional[dict]:
    """
    Returns single project with milestones and student progress.
    """
    project = Project.objects.filter(slug=slug, is_published=True).prefetch_related('milestones').first()
    if not project:
        return None

    user_progress_data = None
    if user and user.is_authenticated:
        up = UserProjectProgress.objects.filter(user=user, project=project).first()
        if up:
            user_progress_data = {
                "status": up.status,
                "current_milestone_order": up.current_milestone_order,
                "completed_milestones": up.completed_milestones or [],
                "submitted_code": up.submitted_code or {},
                "started_at": up.started_at,
                "completed_at": up.completed_at,
            }

    milestones_data = [
        {
            "id": m.id,
            "order": m.order,
            "title": m.title,
            "description": m.description,
            "starter_code": m.starter_code,
            "hints": m.hints or [],
            "xp_reward": m.xp_reward,
        }
        for m in project.milestones.all().order_by('order')
    ]

    return {
        "id": project.id,
        "title": project.title,
        "slug": project.slug,
        "language": project.language,
        "difficulty": project.difficulty,
        "challenge_level": project.challenge_level,
        "short_description": project.short_description,
        "description": project.description,
        "technologies": project.technologies or [],
        "starter_files": project.starter_files or {},
        "xp_reward": project.xp_reward,
        "estimated_minutes": project.estimated_minutes,
        "milestones": milestones_data,
        "user_progress": user_progress_data,
    }

