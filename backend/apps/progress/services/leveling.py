"""
Leveling and progression calculation utilities.
"""
from ..models import LevelRequirement

DEFAULT_LEVELS = [
    (1, 0, "Apprentice"),
    (2, 100, "Junior Coder"),
    (3, 250, "Practitioner"),
    (4, 500, "Specialist"),
    (5, 1000, "Architect"),
    (6, 1750, "Grandmaster"),
]


from django.core.cache import cache

def get_level_requirements():
    cached = cache.get('level_requirements')
    if cached is not None:
        return cached
    requirements = list(LevelRequirement.objects.order_by('level'))
    cache.set('level_requirements', requirements, timeout=86400)  # 24 hours
    return requirements

def calculate_level(total_xp: int) -> dict:
    """
    Computes level, title, base XP, next level target XP, and progress percentage from total XP.
    Reads from LevelRequirement table, falling back to DEFAULT_LEVELS if unseeded.
    """
    db_requirements = get_level_requirements()

    if db_requirements:
        levels = [(r.level, r.xp_threshold, r.title) for r in db_requirements]
    else:
        levels = DEFAULT_LEVELS

    current_lvl = 1
    current_title = levels[0][2]
    current_base_xp = levels[0][1]
    next_level_xp = levels[1][1] if len(levels) > 1 else None

    for i, (lvl, threshold, title) in enumerate(levels):
        if total_xp >= threshold:
            current_lvl = lvl
            current_title = title
            current_base_xp = threshold
            if i + 1 < len(levels):
                next_level_xp = levels[i + 1][1]
            else:
                next_level_xp = None
        else:
            break

    if next_level_xp is not None and next_level_xp > current_base_xp:
        span = next_level_xp - current_base_xp
        gained = total_xp - current_base_xp
        progress_percent = min(100, max(0, round((gained / span) * 100, 1)))
    else:
        progress_percent = 100.0

    return {
        "level": current_lvl,
        "title": current_title,
        "current_level_base_xp": current_base_xp,
        "next_level_xp": next_level_xp,
        "progress_percent": progress_percent,
    }

