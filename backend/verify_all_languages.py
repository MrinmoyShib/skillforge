import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.accounts.models import User
from apps.problems.models import Problem
from apps.submissions.models import Submission, SubmissionStatus
from apps.submissions.tasks import evaluate_submission_task

user = User.objects.filter(is_superuser=False).first()

tests = [
    {
        'lang': 'javascript',
        'prob_id': 101,
        'label': 'JavaScript Unsolved Starter Code',
        'expected_verdict': SubmissionStatus.WRONG_ANSWER,
        'code': 'function twoSum(nums, target) {\n    // Write your code here\n}\n'
    },
    {
        'lang': 'javascript',
        'prob_id': 101,
        'label': 'JavaScript Correct Solution',
        'expected_verdict': SubmissionStatus.ACCEPTED,
        'code': (
            "const fs = require('fs');\n"
            "const input = fs.readFileSync(0, 'utf-8').trim().split(/\\s+/).filter(Boolean);\n"
            "if (input.length >= 2) {\n"
            "    const n = parseInt(input[0], 10);\n"
            "    const target = parseInt(input[1], 10);\n"
            "    const nums = input.slice(2, 2 + n).map(Number);\n"
            "    const map = new Map();\n"
            "    for (let i = 0; i < nums.length; i++) {\n"
            "        const diff = target - nums[i];\n"
            "        if (map.has(diff)) {\n"
            "            console.log(map.get(diff) + ' ' + i);\n"
            "            break;\n"
            "        }\n"
            "        map.set(nums[i], i);\n"
            "    }\n"
            "}\n"
        )
    },
    {
        'lang': 'python',
        'prob_id': 1,
        'label': 'Python Unsolved Starter Code',
        'expected_verdict': SubmissionStatus.WRONG_ANSWER,
        'code': 'def two_sum(nums, target):\n    pass\n'
    },
    {
        'lang': 'python',
        'prob_id': 1,
        'label': 'Python Correct Solution',
        'expected_verdict': SubmissionStatus.ACCEPTED,
        'code': (
            "import sys\n"
            "data = sys.stdin.read().split()\n"
            "if data:\n"
            "    n, target = int(data[0]), int(data[1])\n"
            "    nums = [int(x) for x in data[2:2+n]]\n"
            "    seen = {}\n"
            "    for i, x in enumerate(nums):\n"
            "        diff = target - x\n"
            "        if diff in seen:\n"
            "            print(f'{seen[diff]} {i}')\n"
            "            break\n"
            "        seen[x] = i\n"
        )
    },
    {
        'lang': 'cpp',
        'prob_id': 201,
        'label': 'C++ Unsolved Starter Code',
        'expected_verdict': SubmissionStatus.WRONG_ANSWER,
        'code': (
            "#include <iostream>\n"
            "#include <vector>\n"
            "using namespace std;\n\n"
            "int main() {\n"
            "    // Write your solution here\n"
            "    return 0;\n"
            "}\n"
        )
    },
    {
        'lang': 'cpp',
        'prob_id': 201,
        'label': 'C++ Correct Solution',
        'expected_verdict': SubmissionStatus.ACCEPTED,
        'code': (
            "#include <iostream>\n"
            "#include <vector>\n"
            "#include <unordered_map>\n"
            "using namespace std;\n\n"
            "int main() {\n"
            "    int n, target;\n"
            "    if (cin >> n >> target) {\n"
            "        unordered_map<int, int> seen;\n"
            "        for (int i = 0; i < n; i++) {\n"
            "            int x;\n"
            "            cin >> x;\n"
            "            int diff = target - x;\n"
            "            if (seen.find(diff) != seen.end()) {\n"
            "                cout << seen[diff] << ' ' << i << endl;\n"
            "                break;\n"
            "            }\n"
            "            seen[x] = i;\n"
            "        }\n"
            "    }\n"
            "    return 0;\n"
            "}\n"
        )
    }
]

created_sub_ids = []
all_passed = True

print('\n' + '='*70)
print('MULTI-LANGUAGE SUBMISSION ENGINE VERIFICATION REPORT')
print('='*70)

for t in tests:
    prob = Problem.objects.get(id=t['prob_id'])
    sub = Submission.objects.create(
        user=user,
        problem=prob,
        language=t['lang'],
        source_code=t['code'],
        status=SubmissionStatus.PENDING
    )
    created_sub_ids.append(sub.id)
    evaluate_submission_task(sub.id)
    sub.refresh_from_db()

    passed_ok = (sub.status == t['expected_verdict'])
    if not passed_ok:
        all_passed = False

    status_icon = 'PASS' if passed_ok else 'FAIL'
    print(f"[{status_icon}] {t['label']}:")
    print(f"    Verdict: {sub.status} (expected {t['expected_verdict']})")
    print(f"    Cases Passed: {sub.passed_test_cases_count}/{sub.total_test_cases_count}")
    print(f"    Execution Time: {sub.execution_time}s | Memory: {sub.memory_usage} KB")
    if sub.compile_output:
        print(f"    Compiler Output: {sub.compile_output[:120]}")
    print('-'*70)

# Clean up test rows
Submission.objects.filter(id__in=created_sub_ids).delete()
print(f"OVERALL VERIFICATION: {'ALL 6 TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
print('='*70)

