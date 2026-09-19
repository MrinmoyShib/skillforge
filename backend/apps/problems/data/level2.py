"""
Level 2 Challenges — Scout (Elementary Algorithms & Linear Data Structures)
20 challenges covering two-pointer patterns, frequency maps, prefix sums,
binary search basics, string parsing, and elementary bitwise math.
"""

LEVEL_2_CHALLENGES = [
    {
        'base_slug': 'binary-search',
        'title': 'Binary Search',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['binary-search', 'arrays'],
        'description': (
            "Given a sorted array of `n` integers and a `target` value, return the 0-based index of `target`.\n"
            "If `target` does not exist in the array, print `-1`. Your solution must run in O(log n) time."
        ),
        'input_format': "First line contains two integers `n` and `target`.\nSecond line contains `n` sorted integers.",
        'output_format': "The 0-based index of target or -1.",
        'constraints': "1 <= n <= 10^5\n-10^9 <= a[i], target <= 10^9",
        'examples': [
            {"input": "6 9\n-1 0 3 5 9 12", "output": "4", "explanation": "9 exists at index 4."},
            {"input": "6 2\n-1 0 3 5 9 12", "output": "-1", "explanation": "2 does not exist in nums."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, target;\n"
                "    if (!(cin >> n >> target)) return 0;\n"
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    // Write your solution here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    target = int(data[1])\n"
                "    nums = [int(x) for x in data[2:2+n]]\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const target = parseInt(tokens[1], 10);\n"
                "    const nums = tokens.slice(2, 2 + n).map(Number);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "6 9\n-1 0 3 5 9 12", 'output': "4", 'is_sample': True, 'order': 1},
            {'input': "6 2\n-1 0 3 5 9 12", 'output': "-1", 'is_sample': True, 'order': 2},
            {'input': "1 5\n5", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "5 100\n1 2 3 4 5", 'output': "-1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'maximum-subarray-sum',
        'title': 'Maximum Subarray Sum',
        'difficulty': 'medium',
        'challenge_level': 2,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming', 'arrays'],
        'description': (
            "Given an integer array `nums`, find the contiguous subarray (containing at least one number) "
            "which has the largest sum and print its sum (Kadane's algorithm)."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` space-separated integers.",
        'output_format': "The maximum subarray sum.",
        'constraints': "1 <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        'examples': [
            {"input": "9\n-2 1 -3 4 -1 2 1 -5 4", "output": "6", "explanation": "[4,-1,2,1] has largest sum = 6."},
            {"input": "1\n1", "output": "1", "explanation": "Single element."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<long long> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    // Write your solution here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "9\n-2 1 -3 4 -1 2 1 -5 4", 'output': "6", 'is_sample': True, 'order': 1},
            {'input': "1\n1", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "5\n5 4 -1 7 8", 'output': "23", 'is_sample': False, 'order': 3},
            {'input': "3\n-5 -2 -3", 'output': "-2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'valid-anagram',
        'title': 'Valid Anagram',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['strings', 'hash-table'],
        'description': "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.",
        'input_format': "Two space-separated strings `s` and `t`.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= s.length, t.length <= 10^5\nStrings consist of lowercase English letters.",
        'examples': [
            {"input": "anagram nagaram", "output": "true", "explanation": "Both contain same characters with same frequencies."},
            {"input": "rat car", "output": "false", "explanation": "Different characters."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s, t;\n"
                "    if (cin >> s >> t) {\n"
                "        // Write your solution here\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if len(data) < 2:\n"
                "        return\n"
                "    s, t = data[0], data[1]\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    const [s, t] = tokens;\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "anagram nagaram", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "rat car", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "a a", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "ab a", 'output': "false", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'merge-two-sorted-arrays',
        'title': 'Merge Two Sorted Arrays',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'two-pointers'],
        'description': "Given two sorted integer arrays `nums1` of size `n` and `nums2` of size `m`, merge them into a single sorted array.",
        'input_format': "First line contains `n` and `m`.\nSecond line contains `n` integers.\nThird line contains `m` integers.",
        'output_format': "Space-separated integers representing the merged sorted array.",
        'constraints': "0 <= n, m <= 10^5\n-10^9 <= nums[i] <= 10^9",
        'examples': [
            {"input": "3 3\n1 2 3\n2 5 6", "output": "1 2 2 3 5 6", "explanation": "Combined sorted sequence."},
            {"input": "1 0\n1\n", "output": "1", "explanation": "Second array is empty."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, m;\n"
                "    if (!(cin >> n >> m)) return 0;\n"
                "    vector<int> a(n), b(m);\n"
                "    for (int i = 0; i < n; ++i) cin >> a[i];\n"
                "    for (int i = 0; i < m; ++i) cin >> b[i];\n"
                "    // Write your solution here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    m = int(data[1])\n"
                "    a = [int(x) for x in data[2:2+n]]\n"
                "    b = [int(x) for x in data[2+n:2+n+m]]\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const m = parseInt(tokens[1], 10);\n"
                "    const a = tokens.slice(2, 2 + n).map(Number);\n"
                "    const b = tokens.slice(2 + n, 2 + n + m).map(Number);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 3\n1 2 3\n2 5 6", 'output': "1 2 2 3 5 6", 'is_sample': True, 'order': 1},
            {'input': "1 1\n2\n1", 'output': "1 2", 'is_sample': True, 'order': 2},
            {'input': "2 2\n-5 0\n-3 10", 'output': "-5 -3 0 10", 'is_sample': False, 'order': 3},
            {'input': "3 1\n4 5 6\n1", 'output': "1 4 5 6", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'contains-duplicate',
        'title': 'Contains Duplicate',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'hash-table'],
        'description': "Given an integer array `nums`, return `true` if any value appears at least twice in the array, and `false` if every element is distinct.",
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        'examples': [
            {"input": "4\n1 2 3 1", "output": "true", "explanation": "1 appears twice."},
            {"input": "4\n1 2 3 4", "output": "false", "explanation": "All elements distinct."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <unordered_set>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    // Write your solution here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4\n1 2 3 1", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "4\n1 2 3 4", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "1\n100", 'output': "false", 'is_sample': False, 'order': 3},
            {'input': "5\n1 1 1 1 1", 'output': "true", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'single-number',
        'title': 'Single Number',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'math'],
        'description': "Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.",
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The unique single element.",
        'constraints': "1 <= n <= 3 * 10^4\n-3 * 10^4 <= nums[i] <= 3 * 10^4",
        'examples': [
            {"input": "3\n2 2 1", "output": "1", "explanation": "2 appears twice, 1 appears once."},
            {"input": "5\n4 1 2 1 2", "output": "4", "explanation": "1 and 2 appear twice, 4 is single."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    int ans = 0;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        int x;\n"
                "        cin >> x;\n"
                "        ans ^= x;\n"
                "    }\n"
                "    cout << ans << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    ans = 0\n"
                "    for x in nums:\n"
                "        ans ^= x\n"
                "    print(ans)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    let ans = 0;\n"
                "    for (let i = 1; i <= n; i++) ans ^= parseInt(tokens[i], 10);\n"
                "    console.log(ans);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n2 2 1", 'output': "1", 'is_sample': True, 'order': 1},
            {'input': "5\n4 1 2 1 2", 'output': "4", 'is_sample': True, 'order': 2},
            {'input': "1\n99", 'output': "99", 'is_sample': False, 'order': 3},
            {'input': "7\n-1 -2 -3 -1 -2 -3 42", 'output': "42", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'missing-number',
        'title': 'Missing Number in Sequence',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'math'],
        'description': "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The missing integer.",
        'constraints': "1 <= n <= 10^5\n0 <= nums[i] <= n",
        'examples': [
            {"input": "3\n3 0 1", "output": "2", "explanation": "Range is [0,3], 2 is missing."},
            {"input": "2\n0 1", "output": "2", "explanation": "Range is [0,2], 2 is missing."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    long long expected = (long long)n * (n + 1) / 2;\n"
                "    long long actual = 0;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        long long x;\n"
                "        cin >> x;\n"
                "        actual += x;\n"
                "    }\n"
                "    cout << expected - actual << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    expected = n * (n + 1) // 2\n"
                "    print(expected - sum(nums))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const expected = (n * (n + 1)) / 2;\n"
                "    let sum = 0;\n"
                "    for (let i = 1; i <= n; i++) sum += parseInt(tokens[i], 10);\n"
                "    console.log(expected - sum);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n3 0 1", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "2\n0 1", 'output': "2", 'is_sample': True, 'order': 2},
            {'input': "1\n0", 'output': "1", 'is_sample': False, 'order': 3},
            {'input': "5\n5 4 2 1 0", 'output': "3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'intersection-of-two-arrays',
        'title': 'Intersection of Two Arrays',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'hash-table'],
        'description': (
            "Given two integer arrays `nums1` of size `n` and `nums2` of size `m`, return an array of their "
            "unique intersection elements in sorted order."
        ),
        'input_format': "First line contains `n` and `m`.\nSecond line contains `n` integers.\nThird line contains `m` integers.",
        'output_format': "Space-separated unique intersection elements in ascending order.",
        'constraints': "1 <= n, m <= 10^4\n-10^9 <= nums[i] <= 10^9",
        'examples': [
            {"input": "4 5\n1 2 2 1\n2 2 3 4 5", "output": "2", "explanation": "Common element is 2."},
            {"input": "3 3\n4 9 5\n9 4 9", "output": "4 9", "explanation": "Elements 4 and 9 appear in both."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <set>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, m;\n"
                "    if (!(cin >> n >> m)) return 0;\n"
                "    // Write your solution here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    m = int(data[1])\n"
                "    a = set(int(x) for x in data[2:2+n])\n"
                "    b = set(int(x) for x in data[2+n:2+n+m])\n"
                "    inter = sorted(list(a & b))\n"
                "    print(' '.join(str(x) for x in inter))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const m = parseInt(tokens[1], 10);\n"
                "    const a = new Set(tokens.slice(2, 2 + n).map(Number));\n"
                "    const b = new Set(tokens.slice(2 + n, 2 + n + m).map(Number));\n"
                "    const res = [...a].filter(x => b.has(x)).sort((x, y) => x - y);\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4 5\n1 2 2 1\n2 2 3 4 5", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "3 3\n4 9 5\n9 4 9", 'output': "4 9", 'is_sample': True, 'order': 2},
            {'input': "2 2\n1 2\n3 4", 'output': "", 'is_sample': False, 'order': 3},
            {'input': "3 3\n1 2 3\n1 2 3", 'output': "1 2 3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'move-zeroes',
        'title': 'Move Zeroes to End',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'two-pointers'],
        'description': (
            "Given an integer array `nums`, move all 0's to the end of it while maintaining the relative order "
            "of the non-zero elements."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "Space-separated integers after moving zeroes.",
        'constraints': "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        'examples': [
            {"input": "5\n0 1 0 3 12", "output": "1 3 12 0 0", "explanation": "Zeroes pushed to end."},
            {"input": "1\n0", "output": "0", "explanation": "Only one zero."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    // Write your solution here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5\n0 1 0 3 12", 'output': "1 3 12 0 0", 'is_sample': True, 'order': 1},
            {'input': "1\n0", 'output': "0", 'is_sample': True, 'order': 2},
            {'input': "4\n1 2 3 4", 'output': "1 2 3 4", 'is_sample': False, 'order': 3},
            {'input': "4\n0 0 0 5", 'output': "5 0 0 0", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'remove-duplicates-sorted-array',
        'title': 'Remove Duplicates from Sorted Array',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'two-pointers'],
        'description': "Given a sorted array `nums`, remove duplicates in-place such that each unique element appears only once. Output the unique elements space-separated.",
        'input_format': "First line contains `n`.\nSecond line contains `n` sorted integers.",
        'output_format': "Space-separated unique elements in original sorted order.",
        'constraints': "1 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        'examples': [
            {"input": "3\n1 1 2", "output": "1 2", "explanation": "Unique values are 1 and 2."},
            {"input": "5\n0 0 1 1 2", "output": "0 1 2", "explanation": "Unique values are 0, 1, 2."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    // Write your solution here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n1 1 2", 'output': "1 2", 'is_sample': True, 'order': 1},
            {'input': "5\n0 0 1 1 2", 'output': "0 1 2", 'is_sample': True, 'order': 2},
            {'input': "1\n10", 'output': "10", 'is_sample': False, 'order': 3},
            {'input': "4\n-2 -2 -2 -2", 'output': "-2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'palindrome-string',
        'title': 'Valid Palindrome String',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['strings', 'two-pointers'],
        'description': "A phrase is a palindrome if, after converting all uppercase letters into lowercase and removing all non-alphanumeric characters, it reads the same forward and backward.",
        'input_format': "A single line containing the phrase.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= s.length <= 2 * 10^5",
        'examples': [
            {"input": "A man, a plan, a canal: Panama", "output": "true", "explanation": "'amanaplanacanalpanama' is a palindrome."},
            {"input": "race a car", "output": "false", "explanation": "'raceacar' is not a palindrome."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <cctype>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string line;\n"
                "    if (getline(cin, line)) {\n"
                "        // Write your solution here\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    line = sys.stdin.read().strip()\n"
                "    filtered = [c.lower() for c in line if c.isalnum()]\n"
                "    print('true' if filtered == filtered[::-1] else 'false')\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const line = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    const filtered = line.toLowerCase().replace(/[^a-z0-9]/g, '');\n"
                "    console.log(filtered === filtered.split('').reverse().join('') ? 'true' : 'false');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "A man, a plan, a canal: Panama", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "race a car", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': " ", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "0P", 'output': "false", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'longest-common-prefix',
        'title': 'Longest Common Prefix',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['strings'],
        'description': "Write a function to find the longest common prefix string amongst an array of `n` strings. If there is no common prefix, print an empty string (or empty line).",
        'input_format': "First line contains `n`.\nSecond line contains `n` space-separated strings.",
        'output_format': "The longest common prefix string.",
        'constraints': "1 <= n <= 200\n0 <= strings[i].length <= 200",
        'examples': [
            {"input": "3\nflower flow flight", "output": "fl", "explanation": "'fl' is common to all 3."},
            {"input": "3\ndog racecar car", "output": "", "explanation": "No common prefix."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<string> s(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> s[i];\n"
                "    // Write your solution here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    words = data[1:1+n]\n"
                "    if not words:\n"
                "        print('')\n"
                "        return\n"
                "    prefix = words[0]\n"
                "    for w in words[1:]:\n"
                "        while not w.startswith(prefix):\n"
                "            prefix = prefix[:-1]\n"
                "            if not prefix:\n"
                "                break\n"
                "    print(prefix)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const words = tokens.slice(1, 1 + n);\n"
                "    if (!words.length) { console.log(''); return; }\n"
                "    let prefix = words[0];\n"
                "    for (let i = 1; i < words.length; i++) {\n"
                "        while (words[i].indexOf(prefix) !== 0) {\n"
                "            prefix = prefix.substring(0, prefix.length - 1);\n"
                "            if (!prefix) break;\n"
                "        }\n"
                "    }\n"
                "    console.log(prefix);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\nflower flow flight", 'output': "fl", 'is_sample': True, 'order': 1},
            {'input': "3\ndog racecar car", 'output': "", 'is_sample': True, 'order': 2},
            {'input': "2\ninterspecies interstellar", 'output': "inters", 'is_sample': False, 'order': 3},
            {'input': "1\nalone", 'output': "alone", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'first-unique-character',
        'title': 'First Unique Character in a String',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['strings', 'hash-table'],
        'description': "Given a string `s`, find the first non-repeating character and print its 0-based index. If it does not exist, print `-1`.",
        'input_format': "A single string `s` of lowercase English letters.",
        'output_format': "The 0-based index or -1.",
        'constraints': "1 <= s.length <= 10^5",
        'examples': [
            {"input": "leetcode", "output": "0", "explanation": "'l' is the first unique character."},
            {"input": "loveleetcode", "output": "2", "explanation": "'v' is the first unique character at index 2."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s;\n"
                "    if (cin >> s) {\n"
                "        // Write your solution here\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    s = sys.stdin.read().strip()\n"
                "    if not s:\n"
                "        return\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const s = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!s) return;\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "leetcode", 'output': "0", 'is_sample': True, 'order': 1},
            {'input': "loveleetcode", 'output': "2", 'is_sample': True, 'order': 2},
            {'input': "aabb", 'output': "-1", 'is_sample': False, 'order': 3},
            {'input': "z", 'output': "0", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'majority-element',
        'title': 'Majority Element',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'hash-table'],
        'description': (
            "Given an array `nums` of size `n`, return the majority element.\n"
            "The majority element is the element that appears strictly more than `floor(n / 2)` times."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The majority element.",
        'constraints': "1 <= n <= 5 * 10^4\n-10^9 <= nums[i] <= 10^9",
        'examples': [
            {"input": "3\n3 2 3", "output": "3", "explanation": "3 appears 2 times (> 1.5)."},
            {"input": "7\n2 2 1 1 1 2 2", "output": "2", "explanation": "2 appears 4 times (> 3.5)."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    // Boyer-Moore Voting Algorithm\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n3 2 3", 'output': "3", 'is_sample': True, 'order': 1},
            {'input': "7\n2 2 1 1 1 2 2", 'output': "2", 'is_sample': True, 'order': 2},
            {'input': "1\n50", 'output': "50", 'is_sample': False, 'order': 3},
            {'input': "5\n6 6 6 7 7", 'output': "6", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'prefix-sum-array',
        'title': 'Running Sum / Prefix Sum',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'prefix-sum'],
        'description': "Given an array `nums`, return the running sum of `nums` where `runningSum[i] = sum(nums[0]…nums[i])`.",
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "Space-separated running sums.",
        'constraints': "1 <= n <= 10^5\n-10^6 <= nums[i] <= 10^6",
        'examples': [
            {"input": "4\n1 2 3 4", "output": "1 3 6 10", "explanation": "[1, 1+2, 1+2+3, 1+2+3+4]."},
            {"input": "5\n1 1 1 1 1", "output": "1 2 3 4 5", "explanation": "Cumulative sequence."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    long long current = 0;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        long long x;\n"
                "        cin >> x;\n"
                "        current += x;\n"
                "        cout << current << (i == n - 1 ? \"\" : \" \");\n"
                "    }\n"
                "    cout << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    res = []\n"
                "    cur = 0\n"
                "    for x in nums:\n"
                "        cur += x\n"
                "        res.append(str(cur))\n"
                "    print(' '.join(res))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    let cur = 0;\n"
                "    const res = [];\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        cur += parseInt(tokens[i], 10);\n"
                "        res.push(cur);\n"
                "    }\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4\n1 2 3 4", 'output': "1 3 6 10", 'is_sample': True, 'order': 1},
            {'input': "5\n1 1 1 1 1", 'output': "1 2 3 4 5", 'is_sample': True, 'order': 2},
            {'input': "3\n3 1 2", 'output': "3 4 6", 'is_sample': False, 'order': 3},
            {'input': "2\n-5 5", 'output': "-5 0", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'gcd-and-lcm',
        'title': 'Greatest Common Divisor & LCM',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['math'],
        'description': "Given two positive integers `a` and `b`, find their Greatest Common Divisor (GCD) and Least Common Multiple (LCM).",
        'input_format': "Two space-separated integers `a` and `b`.",
        'output_format': "Two space-separated integers: `GCD LCM`.",
        'constraints': "1 <= a, b <= 10^9",
        'examples': [
            {"input": "12 18", "output": "6 36", "explanation": "GCD(12,18)=6, LCM(12,18)=36."},
            {"input": "5 7", "output": "1 35", "explanation": "Coprime numbers."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <numeric>\n"
                "using namespace std;\n\n"
                "long long gcd_fn(long long a, long long b) {\n"
                "    while (b) { a %= b; swap(a, b); }\n"
                "    return a;\n"
                "}\n\n"
                "int main() {\n"
                "    long long a, b;\n"
                "    if (cin >> a >> b) {\n"
                "        long long g = gcd_fn(a, b);\n"
                "        long long l = (a / g) * b;\n"
                "        cout << g << \" \" << l << \"\\n\";\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nimport math\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if len(data) < 2:\n"
                "        return\n"
                "    a, b = int(data[0]), int(data[1])\n"
                "    g = math.gcd(a, b)\n"
                "    l = (a * b) // g\n"
                "    print(f\"{g} {l}\")\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function gcd(a, b) {\n"
                "    while (b) { let t = b; b = a % b; a = t; }\n"
                "    return a;\n"
                "}\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    const a = BigInt(tokens[0]);\n"
                "    const b = BigInt(tokens[1]);\n"
                "    const g = gcd(a, b);\n"
                "    const l = (a * b) / g;\n"
                "    console.log(`${g.toString()} ${l.toString()}`);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "12 18", 'output': "6 36", 'is_sample': True, 'order': 1},
            {'input': "5 7", 'output': "1 35", 'is_sample': True, 'order': 2},
            {'input': "100 10", 'output': "10 100", 'is_sample': False, 'order': 3},
            {'input': "14 28", 'output': "14 28", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'count-bits',
        'title': 'Counting Set Bits',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['math'],
        'description': "Given a positive integer `n`, count and print the number of '1' bits in its binary representation (also known as the Hamming weight).",
        'input_format': "A single integer `n`.",
        'output_format': "The number of set bits.",
        'constraints': "0 <= n <= 2^31 - 1",
        'examples': [
            {"input": "11", "output": "3", "explanation": "11 in binary is 1011 (three 1s)."},
            {"input": "128", "output": "1", "explanation": "128 in binary is 10000000 (one 1)."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    unsigned int n;\n"
                "    if (cin >> n) {\n"
                "        // Count set bits\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().strip()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data)\n"
                "    print(bin(n).count('1'))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    let n = parseInt(data, 10);\n"
                "    let count = 0;\n"
                "    while (n > 0) {\n"
                "        count += (n & 1);\n"
                "        n = n >>> 1;\n"
                "    }\n"
                "    console.log(count);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "11", 'output': "3", 'is_sample': True, 'order': 1},
            {'input': "128", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "0", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "2147483647", 'output': "31", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'square-root-integer',
        'title': 'Integer Square Root',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['binary-search', 'math'],
        'description': "Given a non-negative integer `x`, return the square root of `x` rounded down to the nearest integer. Do not use built-in sqrt functions.",
        'input_format': "A single integer `x`.",
        'output_format': "The integer square root.",
        'constraints': "0 <= x <= 2^31 - 1",
        'examples': [
            {"input": "4", "output": "2", "explanation": "sqrt(4) = 2."},
            {"input": "8", "output": "2", "explanation": "sqrt(8) = 2.82842..., rounded down is 2."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    long long x;\n"
                "    if (cin >> x) {\n"
                "        // Binary search for integer sqrt\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().strip()\n"
                "    if not data:\n"
                "        return\n"
                "    x = int(data)\n"
                "    # Write binary search here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const x = parseInt(data, 10);\n"
                "    // Write binary search here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "8", 'output': "2", 'is_sample': True, 'order': 2},
            {'input': "0", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "25", 'output': "5", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'rotate-array',
        'title': 'Rotate Array by K Positions',
        'difficulty': 'medium',
        'challenge_level': 2,
        'xp_reward': 100,
        'tag_slugs': ['arrays', 'two-pointers'],
        'description': "Given an array `nums` of size `n`, rotate the array to the right by `k` steps, where `k` is non-negative.",
        'input_format': "First line contains `n` and `k`.\nSecond line contains `n` integers.",
        'output_format': "Space-separated rotated array.",
        'constraints': "1 <= n <= 10^5\n0 <= k <= 10^5\n-10^9 <= nums[i] <= 10^9",
        'examples': [
            {"input": "7 3\n1 2 3 4 5 6 7", "output": "5 6 7 1 2 3 4", "explanation": "Rotated right 3 times."},
            {"input": "4 2\n-1 -100 3 99", "output": "3 99 -1 -100", "explanation": "Rotated right 2 times."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, k;\n"
                "    if (!(cin >> n >> k)) return 0;\n"
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    k %= n;\n"
                "    // Write your rotation logic here\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    k = int(data[1]) % n\n"
                "    nums = [int(x) for x in data[2:2+n]]\n"
                "    rotated = nums[-k:] + nums[:-k] if k > 0 else nums\n"
                "    print(' '.join(str(x) for x in rotated))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    let k = parseInt(tokens[1], 10) % n;\n"
                "    const nums = tokens.slice(2, 2 + n).map(Number);\n"
                "    const rotated = k > 0 ? [...nums.slice(n - k), ...nums.slice(0, n - k)] : nums;\n"
                "    console.log(rotated.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "7 3\n1 2 3 4 5 6 7", 'output': "5 6 7 1 2 3 4", 'is_sample': True, 'order': 1},
            {'input': "4 2\n-1 -100 3 99", 'output': "3 99 -1 -100", 'is_sample': True, 'order': 2},
            {'input': "2 0\n1 2", 'output': "1 2", 'is_sample': False, 'order': 3},
            {'input': "3 4\n1 2 3", 'output': "3 1 2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'climbing-stairs',
        'title': 'Climbing Stairs',
        'difficulty': 'easy',
        'challenge_level': 2,
        'xp_reward': 50,
        'tag_slugs': ['dynamic-programming', 'math'],
        'description': "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        'input_format': "A single integer `n`.",
        'output_format': "The number of distinct ways.",
        'constraints': "1 <= n <= 45",
        'examples': [
            {"input": "2", "output": "2", "explanation": "1 step + 1 step, or 2 steps."},
            {"input": "3", "output": "3", "explanation": "1+1+1, 1+2, 2+1."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (cin >> n) {\n"
                "        // Write DP solution here\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().strip()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data)\n"
                "    if n <= 2:\n"
                "        print(n)\n"
                "        return\n"
                "    a, b = 1, 2\n"
                "    for _ in range(3, n + 1):\n"
                "        a, b = b, a + b\n"
                "    print(b)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    if (n <= 2) { console.log(n); return; }\n"
                "    let a = 1, b = 2;\n"
                "    for (let i = 3; i <= n; i++) {\n"
                "        let temp = a + b;\n"
                "        a = b;\n"
                "        b = temp;\n"
                "    }\n"
                "    console.log(b);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "2", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "3", 'output': "3", 'is_sample': True, 'order': 2},
            {'input': "4", 'output': "5", 'is_sample': False, 'order': 3},
            {'input': "10", 'output': "89", 'is_sample': False, 'order': 4},
        ]
    },
]

