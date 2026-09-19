"""
Level 5 Challenges — Grandmaster & Legend (High-Performance Algorithms & Advanced Mastery)
15 master-tier challenges covering monotonic stacks/deques, binary search optimizations,
bitmask dynamic programming, shortest path graph algorithms, and constraint satisfaction.
"""

LEVEL_5_CHALLENGES = [
    {
        'base_slug': 'trapping-rain-water',
        'title': 'Trapping Rain Water',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['two-pointers', 'stack', 'arrays'],
        'description': (
            "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, "
            "compute how much water it can trap after raining."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` space-separated elevation integers.",
        'output_format': "The total trapped water volume.",
        'constraints': "1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5",
        'examples': [
            {"input": "12\n0 1 0 2 1 0 1 3 2 1 2 1", "output": "6", "explanation": "6 units of rain water trapped."},
            {"input": "6\n4 2 0 3 2 5", "output": "9", "explanation": "9 units of water trapped."}
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
                "    vector<long long> h(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> h[i];\n"
                "    // Two pointers from ends\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n = int(data[0])\n"
                "    h = [int(x) for x in data[1:1+n]]\n"
                "    l, r = 0, n - 1\n"
                "    left_max, right_max = 0, 0\n"
                "    water = 0\n"
                "    while l < r:\n"
                "        if h[l] < h[r]:\n"
                "            if h[l] >= left_max: left_max = h[l]\n"
                "            else: water += left_max - h[l]\n"
                "            l += 1\n"
                "        else:\n"
                "            if h[r] >= right_max: right_max = h[r]\n"
                "            else: water += right_max - h[r]\n"
                "            r -= 1\n"
                "    print(water)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const h = tokens.slice(1, 1 + n).map(Number);\n"
                "    let l = 0, r = n - 1, leftMax = 0, rightMax = 0, water = 0;\n"
                "    while (l < r) {\n"
                "        if (h[l] < h[r]) {\n"
                "            if (h[l] >= leftMax) leftMax = h[l];\n"
                "            else water += leftMax - h[l];\n"
                "            l++;\n"
                "        } else {\n"
                "            if (h[r] >= rightMax) rightMax = h[r];\n"
                "            else water += rightMax - h[r];\n"
                "            r--;\n"
                "        }\n"
                "    }\n"
                "    console.log(water);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "12\n0 1 0 2 1 0 1 3 2 1 2 1", 'output': "6", 'is_sample': True, 'order': 1},
            {'input': "6\n4 2 0 3 2 5", 'output': "9", 'is_sample': True, 'order': 2},
            {'input': "1\n5", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "3\n2 0 2", 'output': "2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'longest-increasing-subsequence',
        'title': 'Longest Increasing Subsequence',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['dynamic-programming', 'binary-search'],
        'description': (
            "Given an integer array `nums`, return the length of the longest strictly increasing subsequence. "
            "Your algorithm should run in O(n log n) time complexity using binary search patience sorting."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The length of the longest strictly increasing subsequence.",
        'constraints': "1 <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        'examples': [
            {"input": "8\n10 9 2 5 3 7 101 18", "output": "4", "explanation": "The longest increasing subsequence is [2, 3, 7, 101], length 4."},
            {"input": "6\n0 1 0 3 2 3", "output": "4", "explanation": "[0, 1, 2, 3] has length 4."}
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
                "    vector<int> tails;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        int x; cin >> x;\n"
                "        auto it = lower_bound(tails.begin(), tails.end(), x);\n"
                "        if (it == tails.end()) tails.push_back(x);\n"
                "        else *it = x;\n"
                "    }\n"
                "    cout << tails.size() << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nimport bisect\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    tails = []\n"
                "    for x in nums:\n"
                "        idx = bisect.bisect_left(tails, x)\n"
                "        if idx == len(tails): tails.append(x)\n"
                "        else: tails[idx] = x\n"
                "    print(len(tails))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function bisectLeft(arr, target) {\n"
                "    let l = 0, r = arr.length;\n"
                "    while (l < r) {\n"
                "        const mid = Math.floor((l + r) / 2);\n"
                "        if (arr[mid] < target) l = mid + 1;\n"
                "        else r = mid;\n"
                "    }\n"
                "    return l;\n"
                "}\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number);\n"
                "    const tails = [];\n"
                "    for (const x of nums) {\n"
                "        const idx = bisectLeft(tails, x);\n"
                "        if (idx === tails.length) tails.push(x);\n"
                "        else tails[idx] = x;\n"
                "    }\n"
                "    console.log(tails.length);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "8\n10 9 2 5 3 7 101 18", 'output': "4", 'is_sample': True, 'order': 1},
            {'input': "6\n0 1 0 3 2 3", 'output': "4", 'is_sample': True, 'order': 2},
            {'input': "1\n7", 'output': "1", 'is_sample': False, 'order': 3},
            {'input': "5\n7 7 7 7 7", 'output': "1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'largest-rectangle-in-histogram',
        'title': 'Largest Rectangle in Histogram',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['stack', 'arrays'],
        'description': (
            "Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, "
            "return the area of the largest rectangle in the histogram in O(n) time using a monotonic stack."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The largest rectangle area.",
        'constraints': "1 <= n <= 10^5\n0 <= heights[i] <= 10^4",
        'examples': [
            {"input": "6\n2 1 5 6 2 3", "output": "10", "explanation": "Bars 5 and 6 form rectangle area = 5 * 2 = 10."},
            {"input": "2\n2 4", "output": "4", "explanation": "Area = 4."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <stack>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<long long> h(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> h[i];\n"
                "    // Monotonic stack\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n = int(data[0])\n"
                "    h = [int(x) for x in data[1:1+n]] + [0]\n"
                "    stack = [-1]\n"
                "    max_area = 0\n"
                "    for i in range(len(h)):\n"
                "        while stack[-1] != -1 and h[stack[-1]] >= h[i]:\n"
                "            height = h[stack.pop()]\n"
                "            width = i - stack[-1] - 1\n"
                "            max_area = max(max_area, height * width)\n"
                "        stack.append(i)\n"
                "    print(max_area)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const h = [...tokens.slice(1, 1 + n).map(Number), 0];\n"
                "    const stack = [-1];\n"
                "    let maxArea = 0;\n"
                "    for (let i = 0; i < h.length; i++) {\n"
                "        while (stack[stack.length - 1] !== -1 && h[stack[stack.length - 1]] >= h[i]) {\n"
                "            const height = h[stack.pop()];\n"
                "            const width = i - stack[stack.length - 1] - 1;\n"
                "            if (height * width > maxArea) maxArea = height * width;\n"
                "        }\n"
                "        stack.push(i);\n"
                "    }\n"
                "    console.log(maxArea);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "6\n2 1 5 6 2 3", 'output': "10", 'is_sample': True, 'order': 1},
            {'input': "2\n2 4", 'output': "4", 'is_sample': True, 'order': 2},
            {'input': "1\n10", 'output': "10", 'is_sample': False, 'order': 3},
            {'input': "5\n1 2 3 4 5", 'output': "9", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'sliding-window-maximum',
        'title': 'Sliding Window Maximum',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['sliding-window', 'stack', 'arrays'],
        'description': (
            "You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the "
            "very left of the array to the very right. Return the max sliding window space-separated in O(n) using a monotonic deque."
        ),
        'input_format': "First line contains `n` and `k`.\nSecond line contains `n` integers.",
        'output_format': "Space-separated maximums for each window.",
        'constraints': "1 <= n <= 10^5\n1 <= k <= n",
        'examples': [
            {"input": "8 3\n1 3 -1 -3 5 3 6 7", "output": "3 3 5 5 6 7", "explanation": "Sliding window of 3 elements."},
            {"input": "1 1\n1", "output": "1", "explanation": "Single item."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <deque>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, k;\n"
                "    if (!(cin >> n >> k)) return 0;\n"
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    // Monotonic deque tracking indices\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nfrom collections import deque\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n, k = int(data[0]), int(data[1])\n"
                "    nums = [int(x) for x in data[2:2+n]]\n"
                "    q = deque()\n"
                "    res = []\n"
                "    for i, x in enumerate(nums):\n"
                "        while q and q[0] <= i - k: q.popleft()\n"
                "        while q and nums[q[-1]] <= x: q.pop()\n"
                "        q.append(i)\n"
                "        if i >= k - 1: res.append(str(nums[q[0]]))\n"
                "    print(' '.join(res))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), k = parseInt(tokens[1], 10);\n"
                "    const nums = tokens.slice(2, 2 + n).map(Number);\n"
                "    const q = [];\n"
                "    const res = [];\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        while (q.length && q[0] <= i - k) q.shift();\n"
                "        while (q.length && nums[q[q.length - 1]] <= nums[i]) q.pop();\n"
                "        q.push(i);\n"
                "        if (i >= k - 1) res.push(nums[q[0]]);\n"
                "    }\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "8 3\n1 3 -1 -3 5 3 6 7", 'output': "3 3 5 5 6 7", 'is_sample': True, 'order': 1},
            {'input': "1 1\n1", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "4 2\n9 11 8 5", 'output': "11 11 8", 'is_sample': False, 'order': 3},
            {'input': "5 5\n1 2 3 4 5", 'output': "5", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'minimum-window-substring',
        'title': 'Minimum Window Substring',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['sliding-window', 'strings', 'hash-table'],
        'description': (
            "Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` "
            "(including duplicates) is included in the window. If there is no such substring, print empty string."
        ),
        'input_format': "Two space-separated strings `s` and `t`.",
        'output_format': "The minimum window substring.",
        'constraints': "1 <= s.length, t.length <= 10^5",
        'examples': [
            {"input": "ADOBECODEBANC ABC", "output": "BANC", "explanation": "Substring 'BANC' includes A, B, and C."},
            {"input": "a a", "output": "a", "explanation": "Exact match."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <unordered_map>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s, t;\n"
                "    if (cin >> s >> t) {\n"
                "        // Two-pointer sliding window with char count\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nfrom collections import Counter\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if len(data) < 2: return\n"
                "    s, t = data[0], data[1]\n"
                "    t_count = Counter(t)\n"
                "    window = {}\n"
                "    have, need = 0, len(t_count)\n"
                "    res, res_len = (-1, -1), float('inf')\n"
                "    l = 0\n"
                "    for r, c in enumerate(s):\n"
                "        window[c] = window.get(c, 0) + 1\n"
                "        if c in t_count and window[c] == t_count[c]:\n"
                "            have += 1\n"
                "        while have == need:\n"
                "            if (r - l + 1) < res_len:\n"
                "                res = (l, r)\n"
                "                res_len = r - l + 1\n"
                "            window[s[l]] -= 1\n"
                "            if s[l] in t_count and window[s[l]] < t_count[s[l]]:\n"
                "                have -= 1\n"
                "            l += 1\n"
                "    l, r = res\n"
                "    print(s[l:r+1] if res_len != float('inf') else '')\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    const [s, t] = tokens;\n"
                "    const tCount = {};\n"
                "    for (const c of t) tCount[c] = (tCount[c] || 0) + 1;\n"
                "    const need = Object.keys(tCount).length;\n"
                "    let have = 0, l = 0, minLen = Infinity, minStart = 0;\n"
                "    const window = {};\n"
                "    for (let r = 0; r < s.length; r++) {\n"
                "        const c = s[r];\n"
                "        window[c] = (window[c] || 0) + 1;\n"
                "        if (tCount[c] && window[c] === tCount[c]) have++;\n"
                "        while (have === need) {\n"
                "            if (r - l + 1 < minLen) { minLen = r - l + 1; minStart = l; }\n"
                "            window[s[l]]--;\n"
                "            if (tCount[s[l]] && window[s[l]] < tCount[s[l]]) have--;\n"
                "            l++;\n"
                "        }\n"
                "    }\n"
                "    console.log(minLen === Infinity ? '' : s.substring(minStart, minStart + minLen));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "ADOBECODEBANC ABC", 'output': "BANC", 'is_sample': True, 'order': 1},
            {'input': "a a", 'output': "a", 'is_sample': True, 'order': 2},
            {'input': "a aa", 'output': "", 'is_sample': False, 'order': 3},
            {'input': "abczba cb", 'output': "bczba", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'median-of-two-sorted-arrays',
        'title': 'Median of Two Sorted Arrays',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['binary-search', 'arrays'],
        'description': (
            "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the "
            "two sorted arrays. The overall run time complexity should be O(log (m+n)). Print result formatted with 1 decimal place (e.g. 2.0 or 2.5)."
        ),
        'input_format': "First line contains `m` and `n`.\nSecond line contains `m` integers.\nThird line contains `n` integers.",
        'output_format': "Median formatted to 1 decimal place.",
        'constraints': "0 <= m, n <= 10^5\nm + n >= 1",
        'examples': [
            {"input": "2 1\n1 3\n2", "output": "2.0", "explanation": "Merged array = [1, 2, 3], median is 2.0."},
            {"input": "2 2\n1 2\n3 4", "output": "2.5", "explanation": "Merged array = [1, 2, 3, 4], median is (2 + 3) / 2 = 2.5."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <iomanip>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int m, n;\n"
                "    if (!(cin >> m >> n)) return 0;\n"
                "    // Binary search on smaller array partition\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    m, n = int(data[0]), int(data[1])\n"
                "    a = [int(x) for x in data[2:2+m]]\n"
                "    b = [int(x) for x in data[2+m:2+m+n]]\n"
                "    if len(a) > len(b): a, b = b, a; m, n = n, m\n"
                "    total = m + n\n"
                "    half = (total + 1) // 2\n"
                "    l, r = 0, m\n"
                "    while l <= r:\n"
                "        i = (l + r) // 2\n"
                "        j = half - i\n"
                "        a_left = a[i - 1] if i > 0 else float('-inf')\n"
                "        a_right = a[i] if i < m else float('inf')\n"
                "        b_left = b[j - 1] if j > 0 else float('-inf')\n"
                "        b_right = b[j] if j < n else float('inf')\n"
                "        if a_left <= b_right and b_left <= a_right:\n"
                "            if total % 2:\n"
                "                print(f\"{max(a_left, b_left):.1f}\")\n"
                "            else:\n"
                "                print(f\"{(max(a_left, b_left) + min(a_right, b_right)) / 2:.1f}\")\n"
                "            return\n"
                "        elif a_left > b_right:\n"
                "            r = i - 1\n"
                "        else:\n"
                "            l = i + 1\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const m = parseInt(tokens[0], 10), n = parseInt(tokens[1], 10);\n"
                "    let a = tokens.slice(2, 2 + m).map(Number);\n"
                "    let b = tokens.slice(2 + m, 2 + m + n).map(Number);\n"
                "    if (a.length > b.length) { const t = a; a = b; b = t; }\n"
                "    const total = a.length + b.length;\n"
                "    const half = Math.floor((total + 1) / 2);\n"
                "    let l = 0, r = a.length;\n"
                "    while (l <= r) {\n"
                "        const i = Math.floor((l + r) / 2);\n"
                "        const j = half - i;\n"
                "        const aLeft = i > 0 ? a[i - 1] : -Infinity;\n"
                "        const aRight = i < a.length ? a[i] : Infinity;\n"
                "        const bLeft = j > 0 ? b[j - 1] : -Infinity;\n"
                "        const bRight = j < b.length ? b[j] : Infinity;\n"
                "        if (aLeft <= bRight && bLeft <= aRight) {\n"
                "            if (total % 2 !== 0) {\n"
                "                console.log(Math.max(aLeft, bLeft).toFixed(1));\n"
                "            } else {\n"
                "                console.log(((Math.max(aLeft, bLeft) + Math.min(aRight, bRight)) / 2).toFixed(1));\n"
                "            }\n"
                "            return;\n"
                "        } else if (aLeft > bRight) {\n"
                "            r = i - 1;\n"
                "        } else {\n"
                "            l = i + 1;\n"
                "        }\n"
                "    }\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "2 1\n1 3\n2", 'output': "2.0", 'is_sample': True, 'order': 1},
            {'input': "2 2\n1 2\n3 4", 'output': "2.5", 'is_sample': True, 'order': 2},
            {'input': "1 0\n10\n", 'output': "10.0", 'is_sample': False, 'order': 3},
            {'input': "3 3\n1 2 5\n3 4 6", 'output': "3.5", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'word-break-ii',
        'title': 'Word Break Problem',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['dynamic-programming', 'strings'],
        'description': (
            "Given a string `s` and a dictionary of `n` strings `wordDict`, return `true` if `s` can be "
            "segmented into a space-separated sequence of one or more dictionary words."
        ),
        'input_format': "First line contains string `s` and integer `n`.\nSecond line contains `n` dictionary words.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= s.length <= 300\n1 <= wordDict.length <= 1000",
        'examples': [
            {"input": "leetcode 2\nleet code", "output": "true", "explanation": "'leetcode' can be segmented into 'leet code'."},
            {"input": "applepenapple 2\napple pen", "output": "true", "explanation": "'apple pen apple'."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <unordered_set>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s;\n"
                "    int n;\n"
                "    if (!(cin >> s >> n)) return 0;\n"
                "    unordered_set<string> dict;\n"
                "    for (int i = 0; i < n; ++i) { string w; cin >> w; dict.insert(w); }\n"
                "    vector<bool> dp(s.length() + 1, false);\n"
                "    dp[0] = true;\n"
                "    for (int i = 1; i <= s.length(); ++i)\n"
                "        for (int j = 0; j < i; ++j)\n"
                "            if (dp[j] && dict.count(s.substr(j, i - j))) { dp[i] = true; break; }\n"
                "    cout << (dp[s.length()] ? \"true\" : \"false\") << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    s, n = data[0], int(data[1])\n"
                "    words = set(data[2:2+n])\n"
                "    dp = [False] * (len(s) + 1)\n"
                "    dp[0] = True\n"
                "    for i in range(1, len(s) + 1):\n"
                "        for j in range(i):\n"
                "            if dp[j] and s[j:i] in words:\n"
                "                dp[i] = True\n"
                "                break\n"
                "    print('true' if dp[len(s)] else 'false')\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const s = tokens[0], n = parseInt(tokens[1], 10);\n"
                "    const words = new Set(tokens.slice(2, 2 + n));\n"
                "    const dp = new Array(s.length + 1).fill(false);\n"
                "    dp[0] = true;\n"
                "    for (let i = 1; i <= s.length; i++) {\n"
                "        for (let j = 0; j < i; j++) {\n"
                "            if (dp[j] && words.has(s.substring(j, i))) {\n"
                "                dp[i] = true;\n"
                "                break;\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    console.log(dp[s.length] ? 'true' : 'false');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "leetcode 2\nleet code", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "applepenapple 2\napple pen", 'output': "true", 'is_sample': True, 'order': 2},
            {'input': "catsandog 5\ncats dog sand and cat", 'output': "false", 'is_sample': False, 'order': 3},
            {'input': "a 1\na", 'output': "true", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'regular-expression-matching',
        'title': 'Regular Expression Matching',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['dynamic-programming', 'strings'],
        'description': (
            "Given an input string `s` and a pattern `p`, implement regular expression matching with support for '.' and '*'.\n"
            "'.' Matches any single character. '*' Matches zero or more of the preceding element. The matching should cover the entire input string."
        ),
        'input_format': "Two space-separated strings `s` and `p`.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= s.length, p.length <= 30",
        'examples': [
            {"input": "aa a*", "output": "true", "explanation": "'*' means zero or more of 'a'."},
            {"input": "ab .* ", "output": "true", "explanation": "'.*' matches any string."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s, p;\n"
                "    if (cin >> s >> p) {\n"
                "        int m = s.length(), n = p.length();\n"
                "        vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));\n"
                "        dp[0][0] = true;\n"
                "        for (int j = 2; j <= n; j += 2) if (p[j - 1] == '*') dp[0][j] = dp[0][j - 2];\n"
                "        for (int i = 1; i <= m; ++i) {\n"
                "            for (int j = 1; j <= n; ++j) {\n"
                "                if (p[j - 1] == '*') {\n"
                "                    dp[i][j] = dp[i][j - 2] || ((p[j - 2] == '.' || p[j - 2] == s[i - 1]) && dp[i - 1][j]);\n"
                "                } else {\n"
                "                    dp[i][j] = (p[j - 1] == '.' || p[j - 1] == s[i - 1]) && dp[i - 1][j - 1];\n"
                "                }\n"
                "            }\n"
                "        }\n"
                "        cout << (dp[m][n] ? \"true\" : \"false\") << \"\\n\";\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if len(data) < 2: return\n"
                "    s, p = data[0], data[1]\n"
                "    m, n = len(s), len(p)\n"
                "    dp = [[False] * (n + 1) for _ in range(m + 1)]\n"
                "    dp[0][0] = True\n"
                "    for j in range(2, n + 1, 2):\n"
                "        if p[j - 1] == '*': dp[0][j] = dp[0][j - 2]\n"
                "    for i in range(1, m + 1):\n"
                "        for j in range(1, n + 1):\n"
                "            if p[j - 1] == '*':\n"
                "                dp[i][j] = dp[i][j - 2] or ((p[j - 2] in ('.', s[i - 1])) and dp[i - 1][j])\n"
                "            else:\n"
                "                dp[i][j] = p[j - 1] in ('.', s[i - 1]) and dp[i - 1][j - 1]\n"
                "    print('true' if dp[m][n] else 'false')\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    const [s, p] = tokens;\n"
                "    const m = s.length, n = p.length;\n"
                "    const dp = Array.from({length: m + 1}, () => new Array(n + 1).fill(false));\n"
                "    dp[0][0] = true;\n"
                "    for (let j = 2; j <= n; j += 2) if (p[j - 1] === '*') dp[0][j] = dp[0][j - 2];\n"
                "    for (let i = 1; i <= m; i++) {\n"
                "        for (let j = 1; j <= n; j++) {\n"
                "            if (p[j - 1] === '*') {\n"
                "                dp[i][j] = dp[i][j - 2] || ((p[j - 2] === '.' || p[j - 2] === s[i - 1]) && dp[i - 1][j]);\n"
                "            } else {\n"
                "                dp[i][j] = (p[j - 1] === '.' || p[j - 1] === s[i - 1]) && dp[i - 1][j - 1];\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    console.log(dp[m][n] ? 'true' : 'false');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "aa a*", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "ab .* ", 'output': "true", 'is_sample': True, 'order': 2},
            {'input': "mississippi mis*is*p*.", 'output': "false", 'is_sample': False, 'order': 3},
            {'input': "a ab*", 'output': "true", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'dijkstra-shortest-path',
        'title': 'Dijkstra Single Source Shortest Path',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['graphs', 'heap'],
        'description': (
            "Given a directed weighted graph with `n` vertices (1 to n) and `m` edges with non-negative weights, "
            "compute the shortest distance from vertex 1 to vertex `n`. If unreachable, print `-1`."
        ),
        'input_format': "First line contains `n` and `m`.\nThe next `m` lines contain `u`, `v`, and `w`.",
        'output_format': "The shortest distance to vertex n or -1.",
        'constraints': "1 <= n <= 10^5\n0 <= m <= 2 * 10^5\n0 <= w <= 10^4",
        'examples': [
            {"input": "4 4\n1 2 2\n1 3 5\n2 4 4\n3 4 1", "output": "6", "explanation": "Path 1->2->4 has weight 2+4=6; path 1->3->4 has weight 5+1=6."},
            {"input": "3 1\n1 2 5", "output": "-1", "explanation": "Vertex 3 unreachable."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <queue>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, m;\n"
                "    if (!(cin >> n >> m)) return 0;\n"
                "    // Dijkstra with priority queue\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nimport heapq\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n, m = int(data[0]), int(data[1])\n"
                "    adj = {i: [] for i in range(1, n + 1)}\n"
                "    idx = 2\n"
                "    for _ in range(m):\n"
                "        u, v, w = int(data[idx]), int(data[idx+1]), int(data[idx+2])\n"
                "        adj[u].append((v, w))\n"
                "        idx += 3\n"
                "    dist = {i: float('inf') for i in range(1, n + 1)}\n"
                "    dist[1] = 0\n"
                "    pq = [(0, 1)]\n"
                "    while pq:\n"
                "        d, u = heapq.heappop(pq)\n"
                "        if d > dist[u]: continue\n"
                "        for v, w in adj[u]:\n"
                "            if dist[u] + w < dist[v]:\n"
                "                dist[v] = dist[u] + w\n"
                "                heapq.heappush(pq, (dist[v], v))\n"
                "    print(dist[n] if dist[n] != float('inf') else -1)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), m = parseInt(tokens[1], 10);\n"
                "    const adj = Array.from({length: n + 1}, () => []);\n"
                "    let idx = 2;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        adj[parseInt(tokens[idx], 10)].push([parseInt(tokens[idx + 1], 10), parseInt(tokens[idx + 2], 10)]);\n"
                "        idx += 3;\n"
                "    }\n"
                "    const dist = new Array(n + 1).fill(Infinity);\n"
                "    dist[1] = 0;\n"
                "    const pq = [[0, 1]];\n"
                "    while (pq.length) {\n"
                "        pq.sort((a, b) => a[0] - b[0]);\n"
                "        const [d, u] = pq.shift();\n"
                "        if (d > dist[u]) continue;\n"
                "        for (const [v, w] of adj[u]) {\n"
                "            if (dist[u] + w < dist[v]) {\n"
                "                dist[v] = dist[u] + w;\n"
                "                pq.push([dist[v], v]);\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    console.log(dist[n] === Infinity ? -1 : dist[n]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4 4\n1 2 2\n1 3 5\n2 4 4\n3 4 1", 'output': "6", 'is_sample': True, 'order': 1},
            {'input': "3 1\n1 2 5", 'output': "-1", 'is_sample': True, 'order': 2},
            {'input': "1 0", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "3 3\n1 2 1\n2 3 2\n1 3 10", 'output': "3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'bellman-ford-shortest-path',
        'title': 'Bellman-Ford Negative Cycle Detection',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['graphs'],
        'description': (
            "Given a directed graph with `n` vertices (1 to n) and `m` edges with weights that may be negative, "
            "determine if the graph contains a negative-weight cycle reachable from vertex 1. Print `true` if negative cycle exists, `false` otherwise."
        ),
        'input_format': "First line contains `n` and `m`.\nThe next `m` lines contain `u`, `v`, and `w`.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= n <= 1000\n0 <= m <= 5000\n-1000 <= w <= 1000",
        'examples': [
            {"input": "3 3\n1 2 1\n2 3 -2\n3 1 -1", "output": "true", "explanation": "Cycle 1->2->3->1 has weight 1 - 2 - 1 = -2 < 0."},
            {"input": "3 2\n1 2 3\n2 3 -1", "output": "false", "explanation": "No cycle."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "struct Edge { int u, v, w; };\n\n"
                "int main() {\n"
                "    int n, m;\n"
                "    if (!(cin >> n >> m)) return 0;\n"
                "    // Bellman-Ford cycle check\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n, m = int(data[0]), int(data[1])\n"
                "    edges = []\n"
                "    idx = 2\n"
                "    for _ in range(m):\n"
                "        edges.append((int(data[idx]), int(data[idx+1]), int(data[idx+2])))\n"
                "        idx += 3\n"
                "    dist = [float('inf')] * (n + 1)\n"
                "    dist[1] = 0\n"
                "    for _ in range(n - 1):\n"
                "        for u, v, w in edges:\n"
                "            if dist[u] != float('inf') and dist[u] + w < dist[v]:\n"
                "                dist[v] = dist[u] + w\n"
                "    has_neg_cycle = False\n"
                "    for u, v, w in edges:\n"
                "        if dist[u] != float('inf') and dist[u] + w < dist[v]:\n"
                "            has_neg_cycle = True\n"
                "            break\n"
                "    print('true' if has_neg_cycle else 'false')\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), m = parseInt(tokens[1], 10);\n"
                "    const edges = [];\n"
                "    let idx = 2;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        edges.push([parseInt(tokens[idx], 10), parseInt(tokens[idx + 1], 10), parseInt(tokens[idx + 2], 10)]);\n"
                "        idx += 3;\n"
                "    }\n"
                "    const dist = new Array(n + 1).fill(Infinity);\n"
                "    dist[1] = 0;\n"
                "    for (let i = 0; i < n - 1; i++) {\n"
                "        for (const [u, v, w] of edges) {\n"
                "            if (dist[u] !== Infinity && dist[u] + w < dist[v]) dist[v] = dist[u] + w;\n"
                "        }\n"
                "    }\n"
                "    let hasCycle = false;\n"
                "    for (const [u, v, w] of edges) {\n"
                "        if (dist[u] !== Infinity && dist[u] + w < dist[v]) { hasCycle = true; break; }\n"
                "    }\n"
                "    console.log(hasCycle ? 'true' : 'false');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 3\n1 2 1\n2 3 -2\n3 1 -1", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "3 2\n1 2 3\n2 3 -1", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "2 1\n1 2 -5", 'output': "false", 'is_sample': False, 'order': 3},
            {'input': "2 2\n1 2 -1\n2 1 -1", 'output': "true", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'network-delay-time',
        'title': 'Network Delay Time',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['graphs', 'heap'],
        'description': (
            "You are given a network of `n` nodes labeled from 1 to `n`. You are also given `times`, a list of travel times "
            "as directed edges `u v w`, and a signal node `k`. Return the minimum time it takes for all the `n` nodes to receive the signal. "
            "If it is impossible for all the nodes to receive the signal, print `-1`."
        ),
        'input_format': "First line contains `n`, `m`, and `k`.\nThe next `m` lines contain `u`, `v`, and `w`.",
        'output_format': "The minimum network propagation delay or -1.",
        'constraints': "1 <= k <= n <= 100\n1 <= times.length <= 6000\n0 <= w <= 100",
        'examples': [
            {"input": "4 3 2\n2 1 1\n2 3 1\n3 4 1", "output": "2", "explanation": "Signal reaches 1 and 3 at t=1, 4 at t=2."},
            {"input": "2 1 1\n1 2 1", "output": "1", "explanation": "Takes 1 unit of time."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <queue>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, m, k;\n"
                "    if (!(cin >> n >> m >> k)) return 0;\n"
                "    // Dijkstra from node k\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nimport heapq\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n, m, k = int(data[0]), int(data[1]), int(data[2])\n"
                "    adj = {i: [] for i in range(1, n + 1)}\n"
                "    idx = 3\n"
                "    for _ in range(m):\n"
                "        u, v, w = int(data[idx]), int(data[idx+1]), int(data[idx+2])\n"
                "        adj[u].append((v, w))\n"
                "        idx += 3\n"
                "    dist = {i: float('inf') for i in range(1, n + 1)}\n"
                "    dist[k] = 0\n"
                "    pq = [(0, k)]\n"
                "    while pq:\n"
                "        d, u = heapq.heappop(pq)\n"
                "        if d > dist[u]: continue\n"
                "        for v, w in adj[u]:\n"
                "            if dist[u] + w < dist[v]:\n"
                "                dist[v] = dist[u] + w\n"
                "                heapq.heappush(pq, (dist[v], v))\n"
                "    max_d = max(dist.values())\n"
                "    print(max_d if max_d != float('inf') else -1)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), m = parseInt(tokens[1], 10), k = parseInt(tokens[2], 10);\n"
                "    const adj = Array.from({length: n + 1}, () => []);\n"
                "    let idx = 3;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        adj[parseInt(tokens[idx], 10)].push([parseInt(tokens[idx + 1], 10), parseInt(tokens[idx + 2], 10)]);\n"
                "        idx += 3;\n"
                "    }\n"
                "    const dist = new Array(n + 1).fill(Infinity);\n"
                "    dist[k] = 0;\n"
                "    const pq = [[0, k]];\n"
                "    while (pq.length) {\n"
                "        pq.sort((a, b) => a[0] - b[0]);\n"
                "        const [d, u] = pq.shift();\n"
                "        if (d > dist[u]) continue;\n"
                "        for (const [v, w] of adj[u]) {\n"
                "            if (dist[u] + w < dist[v]) {\n"
                "                dist[v] = dist[u] + w;\n"
                "                pq.push([dist[v], v]);\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    let maxD = 0;\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        if (dist[i] === Infinity) { console.log(-1); return; }\n"
                "        if (dist[i] > maxD) maxD = dist[i];\n"
                "    }\n"
                "    console.log(maxD);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4 3 2\n2 1 1\n2 3 1\n3 4 1", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "2 1 1\n1 2 1", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "2 1 2\n1 2 1", 'output': "-1", 'is_sample': False, 'order': 3},
            {'input': "3 2 1\n1 2 5\n2 3 3", 'output': "8", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'alien-dictionary',
        'title': 'Alien Dictionary (Topological Order)',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['graphs', 'topological-sort', 'strings'],
        'description': (
            "There is a new alien language that uses the English alphabet. You are given a list of words from the "
            "alien language's dictionary, where the strings are sorted lexicographically according to the rules of this new language.\n"
            "Derive the order of characters and print them concatenated as a string. If the order is invalid (cycle or prefix violation), print empty line."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` space-separated words.",
        'output_format': "The derived alphabet sequence or empty line.",
        'constraints': "1 <= words.length <= 100\n1 <= words[i].length <= 100",
        'examples': [
            {"input": "5\nwrt wrf er ett rftt", "output": "wertf", "explanation": "Valid alien alphabetical order."},
            {"input": "2\nz x", "output": "zx", "explanation": "'z' precedes 'x'."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <unordered_map>\n"
                "#include <unordered_set>\n"
                "#include <queue>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<string> words(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> words[i];\n"
                "    // Directed graph of character precedence\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nfrom collections import defaultdict, deque\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n = int(data[0])\n"
                "    words = data[1:1+n]\n"
                "    adj = defaultdict(set)\n"
                "    indegree = {c: 0 for w in words for c in w}\n"
                "    for i in range(len(words) - 1):\n"
                "        w1, w2 = words[i], words[i+1]\n"
                "        min_len = min(len(w1), len(w2))\n"
                "        if len(w1) > len(w2) and w1.startswith(w2):\n"
                "            print('')\n"
                "            return\n"
                "        for j in range(min_len):\n"
                "            if w1[j] != w2[j]:\n"
                "                if w2[j] not in adj[w1[j]]:\n"
                "                    adj[w1[j]].add(w2[j])\n"
                "                    indegree[w2[j]] += 1\n"
                "                break\n"
                "    q = deque([c for c in indegree if indegree[c] == 0])\n"
                "    res = []\n"
                "    while q:\n"
                "        c = q.popleft()\n"
                "        res.append(c)\n"
                "        for nxt in adj[c]:\n"
                "            indegree[nxt] -= 1\n"
                "            if indegree[nxt] == 0:\n"
                "                q.append(nxt)\n"
                "    if len(res) < len(indegree):\n"
                "        print('')\n"
                "    else:\n"
                "        print(''.join(res))\n\n"
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
                "    const adj = new Map();\n"
                "    const indegree = new Map();\n"
                "    for (const w of words) for (const c of w) { if (!adj.has(c)) adj.set(c, new Set()); indegree.set(c, 0); }\n"
                "    for (let i = 0; i < words.length - 1; i++) {\n"
                "        const w1 = words[i], w2 = words[i + 1];\n"
                "        if (w1.length > w2.length && w1.startsWith(w2)) { console.log(''); return; }\n"
                "        for (let j = 0; j < Math.min(w1.length, w2.length); j++) {\n"
                "            if (w1[j] !== w2[j]) {\n"
                "                if (!adj.get(w1[j]).has(w2[j])) {\n"
                "                    adj.get(w1[j]).add(w2[j]);\n"
                "                    indegree.set(w2[j], indegree.get(w2[j]) + 1);\n"
                "                }\n"
                "                break;\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    const q = [];\n"
                "    for (const [c, deg] of indegree.entries()) if (deg === 0) q.push(c);\n"
                "    const res = [];\n"
                "    while (q.length) {\n"
                "        const c = q.shift();\n"
                "        res.push(c);\n"
                "        for (const nxt of adj.get(c)) {\n"
                "            indegree.set(nxt, indegree.get(nxt) - 1);\n"
                "            if (indegree.get(nxt) === 0) q.push(nxt);\n"
                "        }\n"
                "    }\n"
                "    console.log(res.length === indegree.size ? res.join('') : '');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5\nwrt wrf er ett rftt", 'output': "wertf", 'is_sample': True, 'order': 1},
            {'input': "2\nz x", 'output': "zx", 'is_sample': True, 'order': 2},
            {'input': "3\nz x z", 'output': "", 'is_sample': False, 'order': 3},
            {'input': "1\nabc", 'output': "abc", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'matrix-chain-multiplication',
        'title': 'Matrix Chain Multiplication',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['dynamic-programming'],
        'description': (
            "Given an array `p` of integers where matrix `i` has dimensions `p[i-1] x p[i]` for `1 <= i <= n`, "
            "find the minimum number of scalar multiplications needed to multiply the chain of `n` matrices."
        ),
        'input_format': "First line contains `n` (number of matrices).\nSecond line contains `n + 1` dimension integers.",
        'output_format': "The minimum number of scalar multiplications.",
        'constraints': "1 <= n <= 100\n1 <= p[i] <= 500",
        'examples': [
            {"input": "3\n10 30 5 60", "output": "4500", "explanation": "((A1 x A2) x A3) requires 10*30*5 + 10*5*60 = 1500 + 3000 = 4500 operations."},
            {"input": "4\n40 20 30 10 30", "output": "26000", "explanation": "Optimal parenthesization."}
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
                "    vector<long long> p(n + 1);\n"
                "    for (int i = 0; i <= n; ++i) cin >> p[i];\n"
                "    // Interval DP\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n = int(data[0])\n"
                "    p = [int(x) for x in data[1:2+n]]\n"
                "    dp = [[0] * (n + 1) for _ in range(n + 1)]\n"
                "    for L in range(2, n + 1):\n"
                "        for i in range(1, n - L + 2):\n"
                "            j = i + L - 1\n"
                "            dp[i][j] = float('inf')\n"
                "            for k in range(i, j):\n"
                "                cost = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j]\n"
                "                if cost < dp[i][j]: dp[i][j] = cost\n"
                "    print(dp[1][n])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const p = tokens.slice(1, 2 + n).map(Number);\n"
                "    const dp = Array.from({length: n + 1}, () => new Array(n + 1).fill(0));\n"
                "    for (let L = 2; L <= n; L++) {\n"
                "        for (let i = 1; i <= n - L + 1; i++) {\n"
                "            const j = i + L - 1;\n"
                "            dp[i][j] = Infinity;\n"
                "            for (let k = i; k < j; k++) {\n"
                "                const cost = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j];\n"
                "                if (cost < dp[i][j]) dp[i][j] = cost;\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    console.log(dp[1][n]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n10 30 5 60", 'output': "4500", 'is_sample': True, 'order': 1},
            {'input': "4\n40 20 30 10 30", 'output': "26000", 'is_sample': True, 'order': 2},
            {'input': "1\n10 20", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "2\n10 20 30", 'output': "6000", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'travelling-salesperson',
        'title': 'Travelling Salesperson Problem (Bitmask DP)',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['dynamic-programming', 'graphs'],
        'description': (
            "Given `n` cities (0 to n-1) and an `n x n` distance matrix `dist`, find the minimum cost to visit "
            "every city exactly once and return to starting city 0 (Held-Karp algorithm in O(n^2 2^n))."
        ),
        'input_format': "First line contains `n`.\nThe next `n` lines contain `n` integers each.",
        'output_format': "The minimum tour cost.",
        'constraints': "2 <= n <= 14\n0 <= dist[i][j] <= 1000",
        'examples': [
            {"input": "4\n0 10 15 20\n10 0 35 25\n15 35 0 30\n20 25 30 0", "output": "80", "explanation": "Tour 0->1->3->2->0 has cost 10 + 25 + 30 + 15 = 80."},
            {"input": "3\n0 1 2\n1 0 3\n2 3 0", "output": "6", "explanation": "Tour 0->1->2->0 has cost 1 + 3 + 2 = 6."}
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
                "    // Bitmask Held-Karp\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n = int(data[0])\n"
                "    dist = []\n"
                "    idx = 1\n"
                "    for _ in range(n):\n"
                "        dist.append([int(x) for x in data[idx:idx+n]])\n"
                "        idx += n\n"
                "    memo = {}\n"
                "    def tsp(mask, u):\n"
                "        if mask == (1 << n) - 1:\n"
                "            return dist[u][0]\n"
                "        if (mask, u) in memo:\n"
                "            return memo[(mask, u)]\n"
                "        res = float('inf')\n"
                "        for v in range(n):\n"
                "            if not (mask & (1 << v)):\n"
                "                res = min(res, dist[u][v] + tsp(mask | (1 << v), v))\n"
                "        memo[(mask, u)] = res\n"
                "        return res\n"
                "    print(tsp(1, 0))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const dist = [];\n"
                "    let idx = 1;\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        dist.push(tokens.slice(idx, idx + n).map(Number));\n"
                "        idx += n;\n"
                "    }\n"
                "    const memo = new Map();\n"
                "    function tsp(mask, u) {\n"
                "        if (mask === (1 << n) - 1) return dist[u][0];\n"
                "        const key = (mask << 4) | u;\n"
                "        if (memo.has(key)) return memo.get(key);\n"
                "        let res = Infinity;\n"
                "        for (let v = 0; v < n; v++) {\n"
                "            if (!(mask & (1 << v))) {\n"
                "                const cost = dist[u][v] + tsp(mask | (1 << v), v);\n"
                "                if (cost < res) res = cost;\n"
                "            }\n"
                "        }\n"
                "        memo.set(key, res);\n"
                "        return res;\n"
                "    }\n"
                "    console.log(tsp(1, 0));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4\n0 10 15 20\n10 0 35 25\n15 35 0 30\n20 25 30 0", 'output': "80", 'is_sample': True, 'order': 1},
            {'input': "3\n0 1 2\n1 0 3\n2 3 0", 'output': "6", 'is_sample': True, 'order': 2},
            {'input': "2\n0 5\n5 0", 'output': "10", 'is_sample': False, 'order': 3},
            {'input': "3\n0 10 10\n10 0 10\n10 10 0", 'output': "30", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'n-queens',
        'title': 'N-Queens (Distinct Solutions)',
        'difficulty': 'hard',
        'challenge_level': 5,
        'xp_reward': 200,
        'tag_slugs': ['backtracking'],
        'description': (
            "The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens "
            "attack each other. Given an integer `n`, return the number of distinct solutions to the n-queens puzzle."
        ),
        'input_format': "A single integer `n`.",
        'output_format': "The total number of valid board configurations.",
        'constraints': "1 <= n <= 12",
        'examples': [
            {"input": "4", "output": "2", "explanation": "There are 2 distinct solutions for 4-queens."},
            {"input": "1", "output": "1", "explanation": "Only 1 solution for 1x1 board."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int ans = 0, n;\n"
                "void solveNQueens(int row, int cols, int d1, int d2) {\n"
                "    if (row == n) { ans++; return; }\n"
                "    int avail = ((1 << n) - 1) & ~(cols | d1 | d2);\n"
                "    while (avail) {\n"
                "        int p = avail & -avail;\n"
                "        avail -= p;\n"
                "        solveNQueens(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1);\n"
                "    }\n"
                "}\n\n"
                "int main() {\n"
                "    if (cin >> n) {\n"
                "        solveNQueens(0, 0, 0, 0);\n"
                "        cout << ans << \"\\n\";\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().strip()\n"
                "    if not data: return\n"
                "    n = int(data)\n"
                "    count = 0\n"
                "    def backtrack(row, cols, d1, d2):\n"
                "        nonlocal count\n"
                "        if row == n:\n"
                "            count += 1\n"
                "            return\n"
                "        avail = ((1 << n) - 1) & ~(cols | d1 | d2)\n"
                "        while avail:\n"
                "            p = avail & -avail\n"
                "            avail -= p\n"
                "            backtrack(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1)\n"
                "    backtrack(0, 0, 0, 0)\n"
                "    print(count)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    let count = 0;\n"
                "    function backtrack(row, cols, d1, d2) {\n"
                "        if (row === n) { count++; return; }\n"
                "        let avail = ((1 << n) - 1) & ~(cols | d1 | d2);\n"
                "        while (avail) {\n"
                "            const p = avail & -avail;\n"
                "            avail -= p;\n"
                "            backtrack(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1);\n"
                "        }\n"
                "    }\n"
                "    backtrack(0, 0, 0, 0);\n"
                "    console.log(count);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "1", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "8", 'output': "92", 'is_sample': False, 'order': 3},
            {'input': "5", 'output': "10", 'is_sample': False, 'order': 4},
        ]
    },
]

