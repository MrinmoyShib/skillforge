"""
Master curriculum catalog defining 100 foundational challenges across Levels 1-5,
with native, idiomatic starter codes for Python, JavaScript, and C++, and shared test cases.
Aggregates Level 1 through Level 5 challenge definitions.
"""
from apps.problems.data.level1 import LEVEL_1_CHALLENGES
from apps.problems.data.level2 import LEVEL_2_CHALLENGES
from apps.problems.data.level3 import LEVEL_3_CHALLENGES
from apps.problems.data.level4 import LEVEL_4_CHALLENGES
from apps.problems.data.level5 import LEVEL_5_CHALLENGES

# 100 Core Challenges: 20 Level 1 + 20 Level 2 + 25 Level 3 + 20 Level 4 + 15 Level 5
CORE_CHALLENGES = (
    LEVEL_1_CHALLENGES +
    LEVEL_2_CHALLENGES +
    LEVEL_3_CHALLENGES +
    LEVEL_4_CHALLENGES +
    LEVEL_5_CHALLENGES
)

__all__ = [
    'CORE_CHALLENGES',
    'LEVEL_1_CHALLENGES',
    'LEVEL_2_CHALLENGES',
    'LEVEL_3_CHALLENGES',
    'LEVEL_4_CHALLENGES',
    'LEVEL_5_CHALLENGES',
]

