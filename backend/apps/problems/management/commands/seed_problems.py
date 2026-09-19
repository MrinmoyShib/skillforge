"""
Management command to seed the three core Language Tracks:
1. Python Track (python)
2. JavaScript Track (javascript)
3. C++ Track (cpp)

Populates curated multi-tiered challenges with native starter templates,
category tags, and sample & hidden test cases.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.problems.models import Category, Tag, DifficultyXPConfig, Problem, TestCase
from apps.problems.data.catalog import CORE_CHALLENGES


class Command(BaseCommand):
    help = "Seeds language tracks (Python, JavaScript, C++) and multi-tiered challenges with test cases."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding Difficulty XP Configurations...")
            DifficultyXPConfig.objects.update_or_create(difficulty='easy', defaults={'xp_reward': 50})
            DifficultyXPConfig.objects.update_or_create(difficulty='medium', defaults={'xp_reward': 100})
            DifficultyXPConfig.objects.update_or_create(difficulty='hard', defaults={'xp_reward': 200})

            self.stdout.write("Seeding Language Track Categories...")
            categories = {
                'python': Category.objects.update_or_create(
                    slug='python',
                    defaults={
                        'name': 'Python Track',
                        'description': 'Master Python algorithmic problem solving from syntax foundations to dynamic programming.',
                        'display_order': 1
                    }
                )[0],
                'javascript': Category.objects.update_or_create(
                    slug='javascript',
                    defaults={
                        'name': 'JavaScript Track',
                        'description': 'Modern JavaScript & Node.js data structures, array operations, and algorithm design.',
                        'display_order': 2
                    }
                )[0],
                'cpp': Category.objects.update_or_create(
                    slug='cpp',
                    defaults={
                        'name': 'C++ Track',
                        'description': 'High-performance systems programming, memory-conscious structures, and competitive algorithms.',
                        'display_order': 3
                    }
                )[0],
            }

            self.stdout.write("Seeding Algorithmic Tags...")
            tag_definitions = [
                ('two-pointers', 'Two Pointers'),
                ('hash-table', 'Hash Table'),
                ('dynamic-programming', 'Dynamic Programming'),
                ('loops', 'Loops'),
                ('math', 'Math'),
                ('stack', 'Stack'),
                ('binary-search', 'Binary Search'),
                ('sliding-window', 'Sliding Window'),
                ('heap', 'Heap'),
                ('greedy', 'Greedy'),
                ('sorting', 'Sorting'),
                ('arrays', 'Arrays'),
                ('strings', 'Strings'),
                ('prefix-sum', 'Prefix Sum'),
                ('matrix', 'Matrix'),
                ('backtracking', 'Backtracking'),
                ('tree', 'Binary Tree'),
                ('recursion', 'Recursion'),
                ('graphs', 'Graphs'),
                ('topological-sort', 'Topological Sort'),
                ('bfs', 'BFS / DFS'),
            ]
            tags = {}
            for slug, name in tag_definitions:
                tag_obj, _ = Tag.objects.update_or_create(slug=slug, defaults={'name': name})
                tags[slug] = tag_obj

            tracks = [
                {'lang': 'python', 'prefix': 'py', 'cat': categories['python'], 'time_limit': 3.0},
                {'lang': 'javascript', 'prefix': 'js', 'cat': categories['javascript'], 'time_limit': 3.0},
                {'lang': 'cpp', 'prefix': 'cpp', 'cat': categories['cpp'], 'time_limit': 2.0},
            ]

            total_problems = 0
            total_testcases = 0

            for track in tracks:
                lang = track['lang']
                prefix = track['prefix']
                category = track['cat']
                time_limit = track['time_limit']

                self.stdout.write(f"\n--- Seeding {category.name} ({lang}) ---")

                for ch in CORE_CHALLENGES:
                    slug = f"{prefix}-{ch['base_slug']}"
                    starter_code = ch['starters'].get(lang, '')

                    problem, _ = Problem.objects.update_or_create(
                        slug=slug,
                        defaults={
                            'title': ch['title'],
                            'difficulty': ch['difficulty'],
                            'challenge_level': ch['challenge_level'],
                            'category': category,
                            'xp_reward': ch['xp_reward'],
                            'description': ch['description'],
                            'input_format': ch['input_format'],
                            'output_format': ch['output_format'],
                            'constraints': ch['constraints'],
                            'examples': ch['examples'],
                            'starter_code': starter_code,
                            'language': lang,
                            'time_limit_seconds': time_limit,
                            'memory_limit_kb': 262144,
                            'is_published': True,
                        }
                    )

                    # Attach tags
                    prob_tags = [tags[ts] for ts in ch.get('tag_slugs', []) if ts in tags]
                    if prob_tags:
                        problem.tags.set(prob_tags)

                    # Reset and populate test cases
                    TestCase.objects.filter(problem=problem).delete()
                    tc_objs = [
                        TestCase(
                            problem=problem,
                            input_data=tc['input'],
                            expected_output=tc['output'],
                            is_sample=tc['is_sample'],
                            order=tc['order']
                        )
                        for tc in ch['test_cases']
                    ]
                    TestCase.objects.bulk_create(tc_objs)

                    total_problems += 1
                    total_testcases += len(tc_objs)
                    self.stdout.write(f"  ✓ [{lang.upper()}] {problem.title} (Level {problem.challenge_level}, {len(tc_objs)} test cases)")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully seeded {len(categories)} tracks, {len(tags)} tags, "
                f"{total_problems} challenges, and {total_testcases} test cases across all languages!"
            )
        )
