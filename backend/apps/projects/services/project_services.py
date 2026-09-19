"""
Business logic services for Guided Projects execution and milestone verification.
"""
import logging
from django.db import transaction
from django.utils import timezone
from apps.accounts.models import UserProfile
from apps.progress.models import ActivityLog
from apps.progress.services.leveling import calculate_level
from apps.submissions.models import SubmissionStatus
from apps.submissions.engine import get_execution_engine
from ..models import Project, ProjectMilestone, UserProjectProgress

logger = logging.getLogger(__name__)


def start_project(*, user, project: Project) -> UserProjectProgress:
    """
    Initializes user project enrollment if not already started.
    """
    progress, created = UserProjectProgress.objects.get_or_create(
        user=user,
        project=project,
        defaults={
            'status': 'IN_PROGRESS',
            'current_milestone_order': 1,
            'completed_milestones': [],
            'submitted_code': {},
            'started_at': timezone.now(),
        }
    )
    return progress


def verify_milestone(*, user, project: Project, milestone: ProjectMilestone, source_code: str) -> dict:
    """
    Executes student milestone implementation against the milestone verification test harness.
    Awards XP and advances milestone progress atomically if tests pass.
    """
    # 1. Combine student source code with verification test harness
    if project.language == 'python':
        combined_code = f"{source_code}\n\n# --- AUTOMATED VERIFICATION TEST HARNESS ---\n{milestone.test_harness_code}"
    elif project.language == 'javascript':
        combined_code = f"{source_code}\n\n// --- AUTOMATED VERIFICATION TEST HARNESS ---\n{milestone.test_harness_code}"
    else:
        combined_code = f"{source_code}\n\n// --- AUTOMATED VERIFICATION TEST HARNESS ---\n{milestone.test_harness_code}"

    # 2. Run in sandboxed execution engine
    engine = get_execution_engine()
    result = engine.execute(
        source_code=combined_code,
        language=project.language,
        stdin='',
        expected_output='PASS',
        time_limit=6.0,
        memory_limit=262144
    )

    passed = (result.status == SubmissionStatus.ACCEPTED) or ('PASS' in (result.stdout or ''))

    if not passed:
        diag = result.compile_output or result.stderr or result.stdout or result.error_message or "Output did not match expected verification criteria."
        return {
            "passed": False,
            "message": "Milestone verification failed. Check the diagnostics below.",
            "compile_output": diag,
            "execution_time": result.execution_time,
            "xp_awarded": 0,
            "project_completed": False,
            "next_milestone_order": None,
        }

    # 3. Passed! Update user progress and award XP atomically
    with transaction.atomic():
        progress, _ = UserProjectProgress.objects.select_for_update().get_or_create(
            user=user,
            project=project,
            defaults={
                'status': 'IN_PROGRESS',
                'current_milestone_order': 1,
                'completed_milestones': [],
                'submitted_code': {},
                'started_at': timezone.now(),
            }
        )

        already_completed = milestone.id in progress.completed_milestones
        xp_to_award = 0

        if not already_completed:
            progress.completed_milestones.append(milestone.id)
            xp_to_award += milestone.xp_reward

        # Save submitted code
        submitted_dict = dict(progress.submitted_code or {})
        submitted_dict[str(milestone.id)] = source_code
        progress.submitted_code = submitted_dict

        # Advance milestone order if verifying current milestone
        if milestone.order >= progress.current_milestone_order:
            progress.current_milestone_order = milestone.order + 1

        # Check project completion
        total_milestones = project.milestones.count()
        project_just_completed = False

        if len(progress.completed_milestones) >= total_milestones and progress.status != 'COMPLETED':
            progress.status = 'COMPLETED'
            progress.completed_at = timezone.now()
            xp_to_award += project.xp_reward
            project_just_completed = True

        progress.save()

        # Update user profile XP and level
        if xp_to_award > 0:
            profile = UserProfile.objects.select_for_update().get(user=user)
            profile.total_xp += xp_to_award

            level_info = calculate_level(profile.total_xp)
            profile.current_level = level_info['level']
            profile.save()

            # Activity logging
            if project_just_completed:
                ActivityLog.objects.create(
                    user=user,
                    activity_type=ActivityLog.ActivityType.SOLVE,
                    description=f"Completed Guided Project: {project.title} (+{project.xp_reward} XP)",
                    metadata={
                        "project_id": project.id,
                        "project_slug": project.slug,
                        "language": project.language,
                        "xp_awarded": project.xp_reward,
                    }
                )
            elif not already_completed:
                ActivityLog.objects.create(
                    user=user,
                    activity_type=ActivityLog.ActivityType.SOLVE,
                    description=f"Completed Milestone #{milestone.order} for {project.title} (+{milestone.xp_reward} XP)",
                    metadata={
                        "project_id": project.id,
                        "milestone_id": milestone.id,
                        "milestone_order": milestone.order,
                        "xp_awarded": milestone.xp_reward,
                    }
                )

    return {
        "passed": True,
        "message": f"Milestone #{milestone.order} verified successfully!" if not project_just_completed else f"Project Completed! You earned +{xp_to_award} XP!",
        "compile_output": result.stdout or "All verification tests passed!",
        "execution_time": result.execution_time,
        "xp_awarded": xp_to_award,
        "project_completed": progress.status == 'COMPLETED',
        "next_milestone_order": progress.current_milestone_order if progress.status != 'COMPLETED' else None,
    }
