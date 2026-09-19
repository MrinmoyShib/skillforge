from .analytics import AdminAnalyticsOutputSerializer
from .problems import (
    AdminProblemListSerializer,
    AdminProblemDetailSerializer,
    AdminProblemCreateUpdateSerializer,
    AdminTestCaseSerializer,
    AdminVerifySolutionInputSerializer,
    AdminVerifySolutionOutputSerializer,
)
from .projects import (
    AdminProjectListSerializer,
    AdminProjectDetailSerializer,
    AdminProjectCreateUpdateSerializer,
    AdminProjectMilestoneSerializer,
)
from .users import (
    AdminUserListSerializer,
    AdminUserDetailSerializer,
    AdminUserUpdateSerializer,
    AdminAdjustXPInputSerializer,
)
from .submissions import (
    AdminSubmissionListSerializer,
    AdminSubmissionDetailSerializer,
)

