"""
Level 3 Challenges — Craftsman (Core Algorithmic Thinking & Classic Structures)
25 challenges spanning intervals, two pointers, sliding windows, stacks, matrix traversals,
backtracking permutations/subsets, and fundamental dynamic programming.
"""

LEVEL_3_CHALLENGES = [
    {
        'base_slug': 'merge-intervals',
        'title': 'Merge Overlapping Intervals',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['sorting', 'arrays'],
        'description': (
            "Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, "
            "and return an array of the non-overlapping intervals that cover all the intervals in the input."
        ),
        'input_format': "First line contains `n` (number of intervals).\nThe next `n` lines each contain two integers `start` and `end`.",
        'output_format': "Each merged interval on a new line formatted as `start end` sorted by `start`.",
        'constraints': "1 <= n <= 10^4\n0 <= start_i <= end_i <= 10^5",
        'examples': [
            {"input": "4\n1 3\n2 6\n8 10\n15 18", "output": "1 6\n8 10\n15 18", "explanation": "[1,3] and [2,6] merge into [1,6]."},
            {"input": "2\n1 4\n4 5", "output": "1 5", "explanation": "Touching intervals merge."}
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
                "    vector<pair<int, int>> intervals(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> intervals[i].first >> intervals[i].second;\n"
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
                "    intervals = []\n"
                "    idx = 1\n"
                "    for _ in range(n):\n"
                "        intervals.append([int(data[idx]), int(data[idx+1])])\n"
                "        idx += 2\n"
                "    intervals.sort(key=lambda x: x[0])\n"
                "    merged = []\n"
                "    for interval in intervals:\n"
                "        if not merged or merged[-1][1] < interval[0]:\n"
                "            merged.append(interval)\n"
                "        else:\n"
                "            merged[-1][1] = max(merged[-1][1], interval[1])\n"
                "    for m in merged:\n"
                "        print(f\"{m[0]} {m[1]}\")\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const intervals = [];\n"
                "    let idx = 1;\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        intervals.push([parseInt(tokens[idx], 10), parseInt(tokens[idx+1], 10)]);\n"
                "        idx += 2;\n"
                "    }\n"
                "    intervals.sort((a, b) => a[0] - b[0]);\n"
                "    const merged = [];\n"
                "    for (const inv of intervals) {\n"
                "        if (!merged.length || merged[merged.length - 1][1] < inv[0]) {\n"
                "            merged.push(inv);\n"
                "        } else {\n"
                "            merged[merged.length - 1][1] = Math.max(merged[merged.length - 1][1], inv[1]);\n"
                "        }\n"
                "    }\n"
                "    for (const m of merged) console.log(`${m[0]} ${m[1]}`);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4\n1 3\n2 6\n8 10\n15 18", 'output': "1 6\n8 10\n15 18", 'is_sample': True, 'order': 1},
            {'input': "2\n1 4\n4 5", 'output': "1 5", 'is_sample': True, 'order': 2},
            {'input': "1\n1 10", 'output': "1 10", 'is_sample': False, 'order': 3},
            {'input': "3\n1 10\n2 3\n4 5", 'output': "1 10", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'container-with-most-water',
        'title': 'Container With Most Water',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['two-pointers', 'arrays'],
        'description': (
            "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two "
            "endpoints of the `i`-th line are `(i, 0)` and `(i, height[i])`.\n"
            "Find two lines that together with the x-axis form a container, such that the container contains the most water. "
            "Print the maximum amount of water a container can store."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers representing line heights.",
        'output_format': "The maximum water area.",
        'constraints': "2 <= n <= 10^5\n0 <= height[i] <= 10^4",
        'examples': [
            {"input": "9\n1 8 6 2 5 4 8 3 7", "output": "49", "explanation": "Between index 1 and 8: min(8,7) * (8 - 1) = 7 * 7 = 49."},
            {"input": "2\n1 1", "output": "1", "explanation": "min(1,1) * 1 = 1."}
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
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    h = [int(x) for x in data[1:1+n]]\n"
                "    l, r = 0, n - 1\n"
                "    ans = 0\n"
                "    while l < r:\n"
                "        ans = max(ans, min(h[l], h[r]) * (r - l))\n"
                "        if h[l] < h[r]:\n"
                "            l += 1\n"
                "        else:\n"
                "            r -= 1\n"
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
                "    const h = tokens.slice(1, 1 + n).map(Number);\n"
                "    let l = 0, r = n - 1, ans = 0;\n"
                "    while (l < r) {\n"
                "        const area = Math.min(h[l], h[r]) * (r - l);\n"
                "        if (area > ans) ans = area;\n"
                "        if (h[l] < h[r]) l++;\n"
                "        else r--;\n"
                "    }\n"
                "    console.log(ans);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "9\n1 8 6 2 5 4 8 3 7", 'output': "49", 'is_sample': True, 'order': 1},
            {'input': "2\n1 1", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "4\n4 3 2 1 4", 'output': "16", 'is_sample': False, 'order': 3},
            {'input': "5\n1 2 1 2 1", 'output': "4", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'coin-change',
        'title': 'Coin Change (Min Coins)',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming'],
        'description': (
            "You are given an integer array `coins` representing coins of different denominations and an integer `amount`. "
            "Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up "
            "by any combination of the coins, print `-1`."
        ),
        'input_format': "First line contains `n` (number of coin types) and `amount`.\nSecond line contains `n` coin denominations.",
        'output_format': "The minimum number of coins needed or -1.",
        'constraints': "1 <= coins.length <= 12\n1 <= coins[i] <= 10^4\n0 <= amount <= 10^4",
        'examples': [
            {"input": "3 11\n1 2 5", "output": "3", "explanation": "11 = 5 + 5 + 1 (3 coins)."},
            {"input": "1 3\n2", "output": "-1", "explanation": "Cannot make 3 with only coin 2."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, amount;\n"
                "    if (!(cin >> n >> amount)) return 0;\n"
                "    vector<int> coins(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> coins[i];\n"
                "    // Write unbounded knapsack DP\n"
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
                "    amount = int(data[1])\n"
                "    coins = [int(x) for x in data[2:2+n]]\n"
                "    dp = [float('inf')] * (amount + 1)\n"
                "    dp[0] = 0\n"
                "    for coin in coins:\n"
                "        for i in range(coin, amount + 1):\n"
                "            dp[i] = min(dp[i], dp[i - coin] + 1)\n"
                "    print(dp[amount] if dp[amount] != float('inf') else -1)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const amount = parseInt(tokens[1], 10);\n"
                "    const coins = tokens.slice(2, 2 + n).map(Number);\n"
                "    const dp = new Array(amount + 1).fill(Infinity);\n"
                "    dp[0] = 0;\n"
                "    for (const c of coins) {\n"
                "        for (let i = c; i <= amount; i++) {\n"
                "            if (dp[i - c] + 1 < dp[i]) dp[i] = dp[i - c] + 1;\n"
                "        }\n"
                "    }\n"
                "    console.log(dp[amount] === Infinity ? -1 : dp[amount]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 11\n1 2 5", 'output': "3", 'is_sample': True, 'order': 1},
            {'input': "1 3\n2", 'output': "-1", 'is_sample': True, 'order': 2},
            {'input': "1 0\n1", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "4 6249\n186 419 83 408", 'output': "20", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'house-robber',
        'title': 'House Robber',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming'],
        'description': (
            "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. "
            "Adjacent houses have connected security systems; it will automatically alert police if two adjacent houses are broken into on the same night.\n"
            "Given `n` non-negative integers representing the amount of money in each house, determine the maximum money you can rob tonight without alerting the police."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The maximum money robbable.",
        'constraints': "1 <= n <= 1000\n0 <= nums[i] <= 400",
        'examples': [
            {"input": "4\n1 2 3 1", "output": "4", "explanation": "Rob house 1 (money = 1) and house 3 (money = 3). Total = 4."},
            {"input": "5\n2 7 9 3 1", "output": "12", "explanation": "Rob house 1 (2), house 3 (9), and house 5 (1). Total = 12."}
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
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    // DP logic\n"
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
                "    if not nums:\n"
                "        print(0)\n"
                "        return\n"
                "    rob1, rob2 = 0, 0\n"
                "    for x in nums:\n"
                "        rob1, rob2 = rob2, max(rob1 + x, rob2)\n"
                "    print(rob2)\n\n"
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
                "    let rob1 = 0, rob2 = 0;\n"
                "    for (const x of nums) {\n"
                "        const temp = Math.max(rob1 + x, rob2);\n"
                "        rob1 = rob2;\n"
                "        rob2 = temp;\n"
                "    }\n"
                "    console.log(rob2);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4\n1 2 3 1", 'output': "4", 'is_sample': True, 'order': 1},
            {'input': "5\n2 7 9 3 1", 'output': "12", 'is_sample': True, 'order': 2},
            {'input': "1\n50", 'output': "50", 'is_sample': False, 'order': 3},
            {'input': "2\n2 1", 'output': "2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': '3sum',
        'title': '3Sum (Triplets with Zero Sum)',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['two-pointers', 'arrays', 'sorting'],
        'description': (
            "Given an integer array `nums`, find all unique triplets `[nums[i], nums[j], nums[k]]` such that "
            "`i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n"
            "Output each unique triplet on a new line, space-separated in ascending order within the triplet. "
            "Sort the lines lexicographically."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "Each unique triplet on a new line (space-separated), sorted.",
        'constraints': "3 <= n <= 3000\n-10^5 <= nums[i] <= 10^5",
        'examples': [
            {"input": "6\n-1 0 1 2 -1 -4", "output": "-1 -1 2\n-1 0 1", "explanation": "Unique triplets summing to 0."},
            {"input": "3\n0 1 1", "output": "", "explanation": "No triplet sums to 0."}
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
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    // Sort and use two pointers\n"
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
                "    nums = sorted([int(x) for x in data[1:1+n]])\n"
                "    triplets = []\n"
                "    for i in range(n - 2):\n"
                "        if i > 0 and nums[i] == nums[i - 1]:\n"
                "            continue\n"
                "        l, r = i + 1, n - 1\n"
                "        while l < r:\n"
                "            s = nums[i] + nums[l] + nums[r]\n"
                "            if s < 0:\n"
                "                l += 1\n"
                "            elif s > 0:\n"
                "                r -= 1\n"
                "            else:\n"
                "                triplets.append(f\"{nums[i]} {nums[l]} {nums[r]}\")\n"
                "                while l < r and nums[l] == nums[l + 1]: l += 1\n"
                "                while l < r and nums[r] == nums[r - 1]: r -= 1\n"
                "                l += 1\n"
                "                r -= 1\n"
                "    for t in triplets:\n"
                "        print(t)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number).sort((a, b) => a - b);\n"
                "    const res = [];\n"
                "    for (let i = 0; i < n - 2; i++) {\n"
                "        if (i > 0 && nums[i] === nums[i - 1]) continue;\n"
                "        let l = i + 1, r = n - 1;\n"
                "        while (l < r) {\n"
                "            const s = nums[i] + nums[l] + nums[r];\n"
                "            if (s < 0) l++;\n"
                "            else if (s > 0) r--;\n"
                "            else {\n"
                "                res.push(`${nums[i]} ${nums[l]} ${nums[r]}`);\n"
                "                while (l < r && nums[l] === nums[l + 1]) l++;\n"
                "                while (l < r && nums[r] === nums[r - 1]) r--;\n"
                "                l++; r--;\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    for (const row of res) console.log(row);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "6\n-1 0 1 2 -1 -4", 'output': "-1 -1 2\n-1 0 1", 'is_sample': True, 'order': 1},
            {'input': "3\n0 1 1", 'output': "", 'is_sample': True, 'order': 2},
            {'input': "3\n0 0 0", 'output': "0 0 0", 'is_sample': False, 'order': 3},
            {'input': "5\n-2 0 1 1 2", 'output': "-2 0 2\n-2 1 1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'longest-consecutive-sequence',
        'title': 'Longest Consecutive Sequence',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['hash-table', 'arrays'],
        'description': (
            "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. "
            "You must write an algorithm that runs in O(n) time."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The length of the longest consecutive sequence.",
        'constraints': "0 <= n <= 10^5\n-10^9 <= nums[i] <= 10^9",
        'examples': [
            {"input": "6\n100 4 200 1 3 2", "output": "4", "explanation": "[1, 2, 3, 4] is consecutive of length 4."},
            {"input": "10\n0 3 7 2 5 8 4 6 0 1", "output": "9", "explanation": "[0, 1, 2, 3, 4, 5, 6, 7, 8] has length 9."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <unordered_set>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    unordered_set<long long> s;\n"
                "    for (int i = 0; i < n; ++i) { long long x; cin >> x; s.insert(x); }\n"
                "    // Find longest consecutive sequence\n"
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
                "    nums = set(int(x) for x in data[1:1+n])\n"
                "    ans = 0\n"
                "    for x in nums:\n"
                "        if x - 1 not in nums:\n"
                "            cur = x\n"
                "            streak = 1\n"
                "            while cur + 1 in nums:\n"
                "                cur += 1\n"
                "                streak += 1\n"
                "            ans = max(ans, streak)\n"
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
                "    const nums = new Set(tokens.slice(1, 1 + n).map(Number));\n"
                "    let ans = 0;\n"
                "    for (const x of nums) {\n"
                "        if (!nums.has(x - 1)) {\n"
                "            let cur = x, streak = 1;\n"
                "            while (nums.has(cur + 1)) { cur++; streak++; }\n"
                "            if (streak > ans) ans = streak;\n"
                "        }\n"
                "    }\n"
                "    console.log(ans);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "6\n100 4 200 1 3 2", 'output': "4", 'is_sample': True, 'order': 1},
            {'input': "10\n0 3 7 2 5 8 4 6 0 1", 'output': "9", 'is_sample': True, 'order': 2},
            {'input': "0\n", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "5\n9 1 4 7 3", 'output': "1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'group-anagrams',
        'title': 'Group Anagrams',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['strings', 'hash-table', 'sorting'],
        'description': (
            "Given an array of strings `strs`, group the anagrams together. "
            "For deterministic testing, sort words within each anagram group alphabetically, "
            "and print each group space-separated on a new line, sorted by the first word of each group."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` space-separated lowercase words.",
        'output_format': "Each anagram group on a new line, space-separated.",
        'constraints': "1 <= n <= 10^4\n0 <= strs[i].length <= 100",
        'examples': [
            {"input": "6\neat tea tan ate nat bat", "output": "ate eat tea\nbat\nnat tan", "explanation": "Grouped anagrams."},
            {"input": "1\na", "output": "a", "explanation": "Single word."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <map>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    // Map sorted key -> vector of words\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nfrom collections import defaultdict\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    words = data[1:1+n]\n"
                "    groups = defaultdict(list)\n"
                "    for w in words:\n"
                "        key = ''.join(sorted(w))\n"
                "        groups[key].append(w)\n"
                "    res = [sorted(g) for g in groups.values()]\n"
                "    res.sort(key=lambda x: x[0])\n"
                "    for g in res:\n"
                "        print(' '.join(g))\n\n"
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
                "    const map = new Map();\n"
                "    for (const w of words) {\n"
                "        const key = w.split('').sort().join('');\n"
                "        if (!map.has(key)) map.set(key, []);\n"
                "        map.get(key).push(w);\n"
                "    }\n"
                "    const res = Array.from(map.values()).map(g => g.sort()).sort((a, b) => a[0].localeCompare(b[0]));\n"
                "    for (const g of res) console.log(g.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "6\neat tea tan ate nat bat", 'output': "ate eat tea\nbat\nnat tan", 'is_sample': True, 'order': 1},
            {'input': "1\na", 'output': "a", 'is_sample': True, 'order': 2},
            {'input': "2\ncat tac", 'output': "cat tac", 'is_sample': False, 'order': 3},
            {'input': "3\nabc def ghi", 'output': "abc\ndef\nghi", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'product-of-array-except-self',
        'title': 'Product of Array Except Self',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['arrays', 'prefix-sum'],
        'description': (
            "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all "
            "the elements of `nums` except `nums[i]`. You must write an algorithm that runs in O(n) time and without using the division operation."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "Space-separated products.",
        'constraints': "2 <= n <= 10^5\n-30 <= nums[i] <= 30",
        'examples': [
            {"input": "4\n1 2 3 4", "output": "24 12 8 6", "explanation": "[2*3*4, 1*3*4, 1*2*4, 1*2*3]."},
            {"input": "5\n-1 1 0 -3 3", "output": "0 0 9 0 0", "explanation": "Zero affects products."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<long long> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    // Prefix and suffix product arrays\n"
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
                "    res = [1] * n\n"
                "    prefix = 1\n"
                "    for i in range(n):\n"
                "        res[i] = prefix\n"
                "        prefix *= nums[i]\n"
                "    suffix = 1\n"
                "    for i in range(n - 1, -1, -1):\n"
                "        res[i] *= suffix\n"
                "        suffix *= nums[i]\n"
                "    print(' '.join(str(x) for x in res))\n\n"
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
                "    const res = new Array(n).fill(1);\n"
                "    let prefix = 1;\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        res[i] = prefix;\n"
                "        prefix *= nums[i];\n"
                "    }\n"
                "    let suffix = 1;\n"
                "    for (let i = n - 1; i >= 0; i--) {\n"
                "        res[i] *= suffix;\n"
                "        suffix *= nums[i];\n"
                "    }\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4\n1 2 3 4", 'output': "24 12 8 6", 'is_sample': True, 'order': 1},
            {'input': "5\n-1 1 0 -3 3", 'output': "0 0 9 0 0", 'is_sample': True, 'order': 2},
            {'input': "2\n5 2", 'output': "2 5", 'is_sample': False, 'order': 3},
            {'input': "3\n2 3 4", 'output': "12 8 6", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'spiral-matrix',
        'title': 'Spiral Matrix Traversal',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['matrix', 'arrays'],
        'description': "Given an `m x n` matrix, return all elements of the matrix in spiral order (clockwise starting from top-left).",
        'input_format': "First line contains `m` and `n`.\nThe next `m` lines contain `n` space-separated integers each.",
        'output_format': "Space-separated integers in spiral order.",
        'constraints': "1 <= m, n <= 100\n-100 <= matrix[i][j] <= 100",
        'examples': [
            {"input": "3 3\n1 2 3\n4 5 6\n7 8 9", "output": "1 2 3 6 9 8 7 4 5", "explanation": "Spiral traversal around perimeter inward."},
            {"input": "3 4\n1 2 3 4\n5 6 7 8\n9 10 11 12", "output": "1 2 3 4 8 12 11 10 9 5 6 7", "explanation": "3x4 grid spiral traversal."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int m, n;\n"
                "    if (!(cin >> m >> n)) return 0;\n"
                "    vector<vector<int>> matrix(m, vector<int>(n));\n"
                "    for (int i = 0; i < m; ++i)\n"
                "        for (int j = 0; j < n; ++j) cin >> matrix[i][j];\n"
                "    // Spiral traversal with top, bottom, left, right boundaries\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    m, n = int(data[0]), int(data[1])\n"
                "    grid = []\n"
                "    idx = 2\n"
                "    for _ in range(m):\n"
                "        grid.append([int(x) for x in data[idx:idx+n]])\n"
                "        idx += n\n"
                "    res = []\n"
                "    top, bottom, left, right = 0, m - 1, 0, n - 1\n"
                "    while top <= bottom and left <= right:\n"
                "        for j in range(left, right + 1): res.append(grid[top][j])\n"
                "        top += 1\n"
                "        for i in range(top, bottom + 1): res.append(grid[i][right])\n"
                "        right -= 1\n"
                "        if top <= bottom:\n"
                "            for j in range(right, left - 1, -1): res.append(grid[bottom][j])\n"
                "            bottom -= 1\n"
                "        if left <= right:\n"
                "            for i in range(bottom, top - 1, -1): res.append(grid[i][left])\n"
                "            left += 1\n"
                "    print(' '.join(str(x) for x in res))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const m = parseInt(tokens[0], 10), n = parseInt(tokens[1], 10);\n"
                "    const grid = [];\n"
                "    let idx = 2;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        grid.push(tokens.slice(idx, idx + n).map(Number));\n"
                "        idx += n;\n"
                "    }\n"
                "    const res = [];\n"
                "    let top = 0, bottom = m - 1, left = 0, right = n - 1;\n"
                "    while (top <= bottom && left <= right) {\n"
                "        for (let j = left; j <= right; j++) res.push(grid[top][j]);\n"
                "        top++;\n"
                "        for (let i = top; i <= bottom; i++) res.push(grid[i][right]);\n"
                "        right--;\n"
                "        if (top <= bottom) {\n"
                "            for (let j = right; j >= left; j--) res.push(grid[bottom][j]);\n"
                "            bottom--;\n"
                "        }\n"
                "        if (left <= right) {\n"
                "            for (let i = bottom; i >= top; i--) res.push(grid[i][left]);\n"
                "            left++;\n"
                "        }\n"
                "    }\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 3\n1 2 3\n4 5 6\n7 8 9", 'output': "1 2 3 6 9 8 7 4 5", 'is_sample': True, 'order': 1},
            {'input': "3 4\n1 2 3 4\n5 6 7 8\n9 10 11 12", 'output': "1 2 3 4 8 12 11 10 9 5 6 7", 'is_sample': True, 'order': 2},
            {'input': "1 1\n42", 'output': "42", 'is_sample': False, 'order': 3},
            {'input': "2 2\n1 2\n3 4", 'output': "1 2 4 3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'rotate-matrix',
        'title': 'Rotate Image 90 Degrees',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['matrix', 'arrays'],
        'description': "You are given an `n x n` 2D matrix representing an image, rotate the image by 90 degrees clockwise.",
        'input_format': "First line contains `n`.\nThe next `n` lines contain `n` integers each.",
        'output_format': "The rotated `n x n` matrix with each row on a new line.",
        'constraints': "1 <= n <= 100\n-1000 <= matrix[i][j] <= 1000",
        'examples': [
            {"input": "3\n1 2 3\n4 5 6\n7 8 9", "output": "7 4 1\n8 5 2\n9 6 3", "explanation": "Rotated 90 degrees clockwise."},
            {"input": "2\n1 2\n3 4", "output": "3 1\n4 2", "explanation": "2x2 rotated."}
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
                "    vector<vector<int>> m(n, vector<int>(n));\n"
                "    for (int i = 0; i < n; ++i)\n"
                "        for (int j = 0; j < n; ++j) cin >> m[i][j];\n"
                "    // Transpose then reverse rows\n"
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
                "    m = []\n"
                "    idx = 1\n"
                "    for _ in range(n):\n"
                "        m.append([int(x) for x in data[idx:idx+n]])\n"
                "        idx += n\n"
                "    # Transpose and reverse rows\n"
                "    for i in range(n):\n"
                "        for j in range(i, n):\n"
                "            m[i][j], m[j][i] = m[j][i], m[i][j]\n"
                "    for row in m:\n"
                "        row.reverse()\n"
                "        print(' '.join(str(x) for x in row))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const m = [];\n"
                "    let idx = 1;\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        m.push(tokens.slice(idx, idx + n).map(Number));\n"
                "        idx += n;\n"
                "    }\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        for (let j = i; j < n; j++) {\n"
                "            const t = m[i][j]; m[i][j] = m[j][i]; m[j][i] = t;\n"
                "        }\n"
                "    }\n"
                "    for (const row of m) {\n"
                "        row.reverse();\n"
                "        console.log(row.join(' '));\n"
                "    }\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n1 2 3\n4 5 6\n7 8 9", 'output': "7 4 1\n8 5 2\n9 6 3", 'is_sample': True, 'order': 1},
            {'input': "2\n1 2\n3 4", 'output': "3 1\n4 2", 'is_sample': True, 'order': 2},
            {'input': "1\n5", 'output': "5", 'is_sample': False, 'order': 3},
            {'input': "3\n0 0 1\n0 1 0\n1 0 0", 'output': "1 0 0\n0 1 0\n0 0 1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'set-matrix-zeroes',
        'title': 'Set Matrix Zeroes',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['matrix', 'arrays'],
        'description': "Given an `m x n` integer matrix, if an element is 0, set its entire row and column to 0's.",
        'input_format': "First line contains `m` and `n`.\nThe next `m` lines contain `n` space-separated integers each.",
        'output_format': "The updated matrix with `m` lines.",
        'constraints': "1 <= m, n <= 200\n-2^31 <= matrix[i][j] <= 2^31 - 1",
        'examples': [
            {"input": "3 3\n1 1 1\n1 0 1\n1 1 1", "output": "1 0 1\n0 0 0\n1 0 1", "explanation": "Row 1 and column 1 become zero."},
            {"input": "3 4\n0 1 2 0\n3 4 5 2\n1 3 1 5", "output": "0 0 0 0\n0 4 5 0\n0 3 1 0", "explanation": "Rows and columns containing zeroes wiped."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int m, n;\n"
                "    if (!(cin >> m >> n)) return 0;\n"
                "    vector<vector<long long>> matrix(m, vector<long long>(n));\n"
                "    for (int i = 0; i < m; ++i)\n"
                "        for (int j = 0; j < n; ++j) cin >> matrix[i][j];\n"
                "    // In-place zeroing\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    m, n = int(data[0]), int(data[1])\n"
                "    grid = []\n"
                "    idx = 2\n"
                "    for _ in range(m):\n"
                "        grid.append([int(x) for x in data[idx:idx+n]])\n"
                "        idx += n\n"
                "    zero_rows = set()\n"
                "    zero_cols = set()\n"
                "    for i in range(m):\n"
                "        for j in range(n):\n"
                "            if grid[i][j] == 0:\n"
                "                zero_rows.add(i)\n"
                "                zero_cols.add(j)\n"
                "    for i in range(m):\n"
                "        for j in range(n):\n"
                "            if i in zero_rows or j in zero_cols:\n"
                "                grid[i][j] = 0\n"
                "    for row in grid:\n"
                "        print(' '.join(str(x) for x in row))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const m = parseInt(tokens[0], 10), n = parseInt(tokens[1], 10);\n"
                "    const grid = [];\n"
                "    let idx = 2;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        grid.push(tokens.slice(idx, idx + n).map(Number));\n"
                "        idx += n;\n"
                "    }\n"
                "    const zeroRows = new Set(), zeroCols = new Set();\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        for (let j = 0; j < n; j++) {\n"
                "            if (grid[i][j] === 0) { zeroRows.add(i); zeroCols.add(j); }\n"
                "        }\n"
                "    }\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        for (let j = 0; j < n; j++) {\n"
                "            if (zeroRows.has(i) || zeroCols.has(j)) grid[i][j] = 0;\n"
                "        }\n"
                "    }\n"
                "    for (const row of grid) console.log(row.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 3\n1 1 1\n1 0 1\n1 1 1", 'output': "1 0 1\n0 0 0\n1 0 1", 'is_sample': True, 'order': 1},
            {'input': "3 4\n0 1 2 0\n3 4 5 2\n1 3 1 5", 'output': "0 0 0 0\n0 4 5 0\n0 3 1 0", 'is_sample': True, 'order': 2},
            {'input': "1 1\n0", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "2 2\n1 2\n3 4", 'output': "1 2\n3 4", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'search-in-rotated-sorted-array',
        'title': 'Search in Rotated Sorted Array',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['binary-search', 'arrays'],
        'description': (
            "Given an integer array `nums` sorted in ascending order (with distinct values) that has been rotated "
            "at an unknown pivot index, and an integer `target`, return the 0-based index of `target` or `-1` if not found in O(log n)."
        ),
        'input_format': "First line contains `n` and `target`.\nSecond line contains `n` integers.",
        'output_format': "The index of target or -1.",
        'constraints': "1 <= n <= 10^5\n-10^9 <= nums[i], target <= 10^9",
        'examples': [
            {"input": "7 0\n4 5 6 7 0 1 2", "output": "4", "explanation": "0 is at index 4."},
            {"input": "7 3\n4 5 6 7 0 1 2", "output": "-1", "explanation": "3 is not in array."}
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
                "    // Modified binary search\n"
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
                "    l, r = 0, n - 1\n"
                "    while l <= r:\n"
                "        mid = (l + r) // 2\n"
                "        if nums[mid] == target:\n"
                "            print(mid)\n"
                "            return\n"
                "        if nums[l] <= nums[mid]:\n"
                "            if nums[l] <= target < nums[mid]:\n"
                "                r = mid - 1\n"
                "            else:\n"
                "                l = mid + 1\n"
                "        else:\n"
                "            if nums[mid] < target <= nums[r]:\n"
                "                l = mid + 1\n"
                "            else:\n"
                "                r = mid - 1\n"
                "    print(-1)\n\n"
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
                "    let l = 0, r = n - 1;\n"
                "    while (l <= r) {\n"
                "        const mid = Math.floor((l + r) / 2);\n"
                "        if (nums[mid] === target) { console.log(mid); return; }\n"
                "        if (nums[l] <= nums[mid]) {\n"
                "            if (nums[l] <= target && target < nums[mid]) r = mid - 1;\n"
                "            else l = mid + 1;\n"
                "        } else {\n"
                "            if (nums[mid] < target && target <= nums[r]) l = mid + 1;\n"
                "            else r = mid - 1;\n"
                "        }\n"
                "    }\n"
                "    console.log(-1);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "7 0\n4 5 6 7 0 1 2", 'output': "4", 'is_sample': True, 'order': 1},
            {'input': "7 3\n4 5 6 7 0 1 2", 'output': "-1", 'is_sample': True, 'order': 2},
            {'input': "1 0\n0", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "3 1\n3 1 2", 'output': "1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'find-peak-element',
        'title': 'Find Peak Element',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['binary-search', 'arrays'],
        'description': (
            "A peak element is an element that is strictly greater than its neighbors.\n"
            "Given a 0-indexed integer array `nums`, find any peak element, and print its index in O(log n) time."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The index of any peak element.",
        'constraints': "1 <= n <= 10^5\n-2^31 <= nums[i] <= 2^31 - 1\nnums[i] != nums[i + 1] for all valid i",
        'examples': [
            {"input": "4\n1 2 3 1", "output": "2", "explanation": "3 is a peak at index 2."},
            {"input": "7\n1 2 1 3 5 6 4", "output": "5", "explanation": "Index 5 (value 6) is a peak."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<long long> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    int l = 0, r = n - 1;\n"
                "    while (l < r) {\n"
                "        int mid = (l + r) / 2;\n"
                "        if (nums[mid] > nums[mid + 1]) r = mid;\n"
                "        else l = mid + 1;\n"
                "    }\n"
                "    cout << l << \"\\n\";\n"
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
                "    l, r = 0, n - 1\n"
                "    while l < r:\n"
                "        mid = (l + r) // 2\n"
                "        if nums[mid] > nums[mid + 1]:\n"
                "            r = mid\n"
                "        else:\n"
                "            l = mid + 1\n"
                "    print(l)\n\n"
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
                "    let l = 0, r = n - 1;\n"
                "    while (l < r) {\n"
                "        const mid = Math.floor((l + r) / 2);\n"
                "        if (nums[mid] > nums[mid + 1]) r = mid;\n"
                "        else l = mid + 1;\n"
                "    }\n"
                "    console.log(l);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4\n1 2 3 1", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "7\n1 2 1 3 5 6 4", 'output': "5", 'is_sample': True, 'order': 2},
            {'input': "1\n10", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "3\n1 3 2", 'output': "1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'min-stack',
        'title': 'Min Stack Operations',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['stack'],
        'description': (
            "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time O(1).\n"
            "Given `q` operations: `push x`, `pop`, `top`, or `getMin`, process them and print the results of `top` and `getMin` on new lines."
        ),
        'input_format': "First line contains `q`.\nThe next `q` lines each contain an operation (`push x`, `pop`, `top`, `getMin`).",
        'output_format': "The outputs of each `top` and `getMin` query.",
        'constraints': "1 <= q <= 10^4\n-2^31 <= x <= 2^31 - 1",
        'examples': [
            {"input": "7\npush -2\npush 0\npush -3\ngetMin\npop\ntop\ngetMin", "output": "-3\n0\n-2", "explanation": "Standard min stack execution."},
            {"input": "3\npush 5\ntop\ngetMin", "output": "5\n5", "explanation": "Single item stack."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <stack>\n"
                "#include <string>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int q;\n"
                "    if (!(cin >> q)) return 0;\n"
                "    stack<int> s, min_s;\n"
                "    while (q--) {\n"
                "        string op;\n"
                "        cin >> op;\n"
                "        // Handle commands\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    lines = sys.stdin.read().strip().split('\\n')\n"
                "    if not lines or not lines[0]:\n"
                "        return\n"
                "    q = int(lines[0])\n"
                "    stack = []\n"
                "    min_stack = []\n"
                "    for i in range(1, q + 1):\n"
                "        parts = lines[i].split()\n"
                "        op = parts[0]\n"
                "        if op == 'push':\n"
                "            val = int(parts[1])\n"
                "            stack.append(val)\n"
                "            min_stack.append(min(val, min_stack[-1] if min_stack else val))\n"
                "        elif op == 'pop':\n"
                "            stack.pop()\n"
                "            min_stack.pop()\n"
                "        elif op == 'top':\n"
                "            print(stack[-1])\n"
                "        elif op == 'getMin':\n"
                "            print(min_stack[-1])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const lines = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n"
                "    if (!lines.length || !lines[0]) return;\n"
                "    const q = parseInt(lines[0], 10);\n"
                "    const stack = [], minStack = [];\n"
                "    for (let i = 1; i <= q; i++) {\n"
                "        const parts = lines[i].trim().split(/\\s+/);\n"
                "        const op = parts[0];\n"
                "        if (op === 'push') {\n"
                "            const val = parseInt(parts[1], 10);\n"
                "            stack.push(val);\n"
                "            minStack.push(minStack.length ? Math.min(val, minStack[minStack.length - 1]) : val);\n"
                "        } else if (op === 'pop') {\n"
                "            stack.pop(); minStack.pop();\n"
                "        } else if (op === 'top') {\n"
                "            console.log(stack[stack.length - 1]);\n"
                "        } else if (op === 'getMin') {\n"
                "            console.log(minStack[minStack.length - 1]);\n"
                "        }\n"
                "    }\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "7\npush -2\npush 0\npush -3\ngetMin\npop\ntop\ngetMin", 'output': "-3\n0\n-2", 'is_sample': True, 'order': 1},
            {'input': "3\npush 5\ntop\ngetMin", 'output': "5\n5", 'is_sample': True, 'order': 2},
            {'input': "4\npush 1\npush 2\ngetMin\ntop", 'output': "1\n2", 'is_sample': False, 'order': 3},
            {'input': "5\npush 10\npush 20\npush 5\ngetMin\npop", 'output': "5", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'evaluate-reverse-polish-notation',
        'title': 'Evaluate Reverse Polish Notation (RPN)',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['stack', 'math'],
        'description': (
            "Evaluate the value of an arithmetic expression in Reverse Polish Notation (tokens separated by spaces).\n"
            "Valid operators are `+`, `-`, `*`, and `/`. Division truncates toward zero."
        ),
        'input_format': "A single line containing space-separated tokens.",
        'output_format': "The integer result of the evaluation.",
        'constraints': "1 <= tokens.length <= 10^4",
        'examples': [
            {"input": "2 1 + 3 *", "output": "9", "explanation": "((2 + 1) * 3) = 9."},
            {"input": "4 13 5 / +", "output": "6", "explanation": "(4 + (13 / 5)) = 6."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <stack>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string token;\n"
                "    stack<long long> s;\n"
                "    while (cin >> token) {\n"
                "        // Evaluate RPN\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    tokens = sys.stdin.read().split()\n"
                "    if not tokens:\n"
                "        return\n"
                "    stack = []\n"
                "    for t in tokens:\n"
                "        if t in '+-*/':\n"
                "            b = stack.pop()\n"
                "            a = stack.pop()\n"
                "            if t == '+': stack.append(a + b)\n"
                "            elif t == '-': stack.append(a - b)\n"
                "            elif t == '*': stack.append(a * b)\n"
                "            elif t == '/': stack.append(int(a / b))\n"
                "        else:\n"
                "            stack.append(int(t))\n"
                "    print(stack[-1])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const stack = [];\n"
                "    for (const t of tokens) {\n"
                "        if (['+', '-', '*', '/'].includes(t)) {\n"
                "            const b = stack.pop(), a = stack.pop();\n"
                "            if (t === '+') stack.push(a + b);\n"
                "            else if (t === '-') stack.push(a - b);\n"
                "            else if (t === '*') stack.push(a * b);\n"
                "            else if (t === '/') stack.push(Math.trunc(a / b));\n"
                "        } else {\n"
                "            stack.push(parseInt(t, 10));\n"
                "        }\n"
                "    }\n"
                "    console.log(stack[stack.length - 1]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "2 1 + 3 *", 'output': "9", 'is_sample': True, 'order': 1},
            {'input': "4 13 5 / +", 'output': "6", 'is_sample': True, 'order': 2},
            {'input': "10 6 9 3 + -11 * / * 17 + 5 +", 'output': "22", 'is_sample': False, 'order': 3},
            {'input': "3", 'output': "3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'daily-temperatures',
        'title': 'Daily Temperatures (Next Warmer Day)',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['stack', 'arrays'],
        'description': (
            "Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` "
            "such that `answer[i]` is the number of days you have to wait after the `i`-th day to get a warmer temperature. "
            "If there is no future day for which this is possible, keep `answer[i] == 0` instead."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` space-separated temperatures.",
        'output_format': "Space-separated wait days.",
        'constraints': "1 <= n <= 10^5\n30 <= temperatures[i] <= 100",
        'examples': [
            {"input": "8\n73 74 75 71 69 72 76 73", "output": "1 1 4 2 1 1 0 0", "explanation": "Days until a strictly warmer temperature."},
            {"input": "4\n30 40 50 60", "output": "1 1 1 0", "explanation": "Monotonically increasing."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <stack>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<int> t(n), ans(n, 0);\n"
                "    for (int i = 0; i < n; ++i) cin >> t[i];\n"
                "    // Monotonic stack\n"
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
                "    temps = [int(x) for x in data[1:1+n]]\n"
                "    ans = [0] * n\n"
                "    stack = []\n"
                "    for i, t in enumerate(temps):\n"
                "        while stack and temps[stack[-1]] < t:\n"
                "            prev_idx = stack.pop()\n"
                "            ans[prev_idx] = i - prev_idx\n"
                "        stack.append(i)\n"
                "    print(' '.join(str(x) for x in ans))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const temps = tokens.slice(1, 1 + n).map(Number);\n"
                "    const ans = new Array(n).fill(0);\n"
                "    const stack = [];\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        while (stack.length && temps[stack[stack.length - 1]] < temps[i]) {\n"
                "            const prev = stack.pop();\n"
                "            ans[prev] = i - prev;\n"
                "        }\n"
                "        stack.push(i);\n"
                "    }\n"
                "    console.log(ans.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "8\n73 74 75 71 69 72 76 73", 'output': "1 1 4 2 1 1 0 0", 'is_sample': True, 'order': 1},
            {'input': "4\n30 40 50 60", 'output': "1 1 1 0", 'is_sample': True, 'order': 2},
            {'input': "3\n30 60 90", 'output': "1 1 0", 'is_sample': False, 'order': 3},
            {'input': "3\n90 80 70", 'output': "0 0 0", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'jump-game',
        'title': 'Jump Game (Can Reach End)',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['greedy', 'arrays'],
        'description': (
            "You are given an integer array `nums`. You are initially positioned at the array's first index, "
            "and each element in the array represents your maximum jump length at that position.\n"
            "Print `true` if you can reach the last index, or `false` otherwise."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= n <= 10^5\n0 <= nums[i] <= 10^5",
        'examples': [
            {"input": "5\n2 3 1 1 4", "output": "true", "explanation": "Jump 1 step to index 1, then 3 steps to the last index."},
            {"input": "5\n3 2 1 0 4", "output": "false", "explanation": "You will always arrive at index 3, whose jump is 0."}
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
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    // Greedy reachable limit\n"
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
                "    reach = 0\n"
                "    for i, x in enumerate(nums):\n"
                "        if i > reach:\n"
                "            print('false')\n"
                "            return\n"
                "        reach = max(reach, i + x)\n"
                "    print('true')\n\n"
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
                "    let reach = 0;\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        if (i > reach) { console.log('false'); return; }\n"
                "        reach = Math.max(reach, i + nums[i]);\n"
                "    }\n"
                "    console.log('true');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5\n2 3 1 1 4", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "5\n3 2 1 0 4", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "1\n0", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "4\n1 0 1 0", 'output': "false", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'gas-station',
        'title': 'Gas Station Circuit',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['greedy', 'arrays'],
        'description': (
            "There are `n` gas stations along a circular route, where the amount of gas at the `i`-th station is `gas[i]`.\n"
            "You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `i`-th station to its next `(i + 1)`-th station.\n"
            "Return the starting gas station's 0-based index if you can travel around the circuit once in the clockwise direction, otherwise return -1."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers (`gas`).\nThird line contains `n` integers (`cost`).",
        'output_format': "Starting index or -1.",
        'constraints': "1 <= n <= 10^5\n0 <= gas[i], cost[i] <= 10^4",
        'examples': [
            {"input": "5\n1 2 3 4 5\n3 4 5 1 2", "output": "3", "explanation": "Start at station 3 (index 3)."},
            {"input": "3\n2 3 4\n3 4 3", "output": "-1", "explanation": "Total gas < total cost."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<int> gas(n), cost(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> gas[i];\n"
                "    for (int i = 0; i < n; ++i) cin >> cost[i];\n"
                "    // Greedy single pass\n"
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
                "    gas = [int(x) for x in data[1:1+n]]\n"
                "    cost = [int(x) for x in data[1+n:1+2*n]]\n"
                "    if sum(gas) < sum(cost):\n"
                "        print(-1)\n"
                "        return\n"
                "    total, start = 0, 0\n"
                "    for i in range(n):\n"
                "        total += gas[i] - cost[i]\n"
                "        if total < 0:\n"
                "            total = 0\n"
                "            start = i + 1\n"
                "    print(start)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const gas = tokens.slice(1, 1 + n).map(Number);\n"
                "    const cost = tokens.slice(1 + n, 1 + 2 * n).map(Number);\n"
                "    let totalGas = 0, totalCost = 0;\n"
                "    for (let i = 0; i < n; i++) { totalGas += gas[i]; totalCost += cost[i]; }\n"
                "    if (totalGas < totalCost) { console.log(-1); return; }\n"
                "    let cur = 0, start = 0;\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        cur += gas[i] - cost[i];\n"
                "        if (cur < 0) { cur = 0; start = i + 1; }\n"
                "    }\n"
                "    console.log(start);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5\n1 2 3 4 5\n3 4 5 1 2", 'output': "3", 'is_sample': True, 'order': 1},
            {'input': "3\n2 3 4\n3 4 3", 'output': "-1", 'is_sample': True, 'order': 2},
            {'input': "1\n5\n4", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "2\n1 2\n2 1", 'output': "1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'subsets',
        'title': 'Generate All Subsets (Power Set)',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['backtracking', 'arrays'],
        'description': (
            "Given an integer array `nums` of unique elements, return all possible subsets (the power set).\n"
            "Sort each subset in ascending order, and print each subset on a new line (empty line for empty set). "
            "Sort the lines by size, then lexicographically."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` unique integers.",
        'output_format': "Each subset space-separated on a new line.",
        'constraints': "1 <= n <= 10\n-10 <= nums[i] <= 10",
        'examples': [
            {"input": "3\n1 2 3", "output": "\n1\n2\n3\n1 2\n1 3\n2 3\n1 2 3", "explanation": "All 2^3 = 8 subsets."},
            {"input": "1\n0", "output": "\n0", "explanation": "Empty set and [0]."}
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
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    // Generate power set\n"
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
                "    nums = sorted([int(x) for x in data[1:1+n]])\n"
                "    subsets = []\n"
                "    for mask in range(1 << n):\n"
                "        sub = [nums[i] for i in range(n) if (mask & (1 << i))]\n"
                "        subsets.append(sub)\n"
                "    subsets.sort(key=lambda x: (len(x), x))\n"
                "    for sub in subsets:\n"
                "        print(' '.join(str(x) for x in sub))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number).sort((a, b) => a - b);\n"
                "    const subsets = [];\n"
                "    for (let mask = 0; mask < (1 << n); mask++) {\n"
                "        const sub = [];\n"
                "        for (let i = 0; i < n; i++) {\n"
                "            if (mask & (1 << i)) sub.push(nums[i]);\n"
                "        }\n"
                "        subsets.push(sub);\n"
                "    }\n"
                "    subsets.sort((a, b) => {\n"
                "        if (a.length !== b.length) return a.length - b.length;\n"
                "        for (let i = 0; i < a.length; i++) {\n"
                "            if (a[i] !== b[i]) return a[i] - b[i];\n"
                "        }\n"
                "        return 0;\n"
                "    });\n"
                "    for (const sub of subsets) console.log(sub.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n1 2 3", 'output': "\n1\n2\n3\n1 2\n1 3\n2 3\n1 2 3", 'is_sample': True, 'order': 1},
            {'input': "1\n0", 'output': "\n0", 'is_sample': True, 'order': 2},
            {'input': "2\n1 2", 'output': "\n1\n2\n1 2", 'is_sample': False, 'order': 3},
            {'input': "2\n5 10", 'output': "\n5\n10\n5 10", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'permutations',
        'title': 'Permutations of Array',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['backtracking', 'arrays'],
        'description': (
            "Given an array `nums` of distinct integers, return all the possible permutations in lexicographical order.\n"
            "Each permutation should be printed space-separated on a new line."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "All permutations, one per line.",
        'constraints': "1 <= n <= 8\n-10 <= nums[i] <= 10",
        'examples': [
            {"input": "3\n1 2 3", "output": "1 2 3\n1 3 2\n2 1 3\n2 3 1\n3 1 2\n3 2 1", "explanation": "3! = 6 permutations."},
            {"input": "2\n0 1", "output": "0 1\n1 0", "explanation": "2! = 2 permutations."}
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
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n"
                "    sort(nums.begin(), nums.end());\n"
                "    do {\n"
                "        for (int i = 0; i < n; ++i) cout << nums[i] << (i == n - 1 ? \"\" : \" \");\n"
                "        cout << \"\\n\";\n"
                "    } while (next_permutation(nums.begin(), nums.end()));\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nfrom itertools import permutations\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n = int(data[0])\n"
                "    nums = sorted([int(x) for x in data[1:1+n]])\n"
                "    for p in permutations(nums):\n"
                "        print(' '.join(str(x) for x in p))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function permute(arr) {\n"
                "    if (arr.length <= 1) return [arr];\n"
                "    const res = [];\n"
                "    for (let i = 0; i < arr.length; i++) {\n"
                "        const rest = [...arr.slice(0, i), ...arr.slice(i + 1)];\n"
                "        for (const sub of permute(rest)) {\n"
                "            res.push([arr[i], ...sub]);\n"
                "        }\n"
                "    }\n"
                "    return res;\n"
                "}\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const nums = tokens.slice(1, 1 + n).map(Number).sort((a, b) => a - b);\n"
                "    const perms = permute(nums);\n"
                "    for (const p of perms) console.log(p.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n1 2 3", 'output': "1 2 3\n1 3 2\n2 1 3\n2 3 1\n3 1 2\n3 2 1", 'is_sample': True, 'order': 1},
            {'input': "2\n0 1", 'output': "0 1\n1 0", 'is_sample': True, 'order': 2},
            {'input': "1\n5", 'output': "5", 'is_sample': False, 'order': 3},
            {'input': "2\n3 2", 'output': "2 3\n3 2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'combination-sum',
        'title': 'Combination Sum',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['backtracking', 'arrays'],
        'description': (
            "Given an array of distinct integers `candidates` and a target integer `target`, return a list of all "
            "unique combinations of `candidates` where the chosen numbers sum to `target`.\n"
            "The same number may be chosen unlimited times. Print each combination space-separated on a new line."
        ),
        'input_format': "First line contains `n` and `target`.\nSecond line contains `n` distinct candidates.",
        'output_format': "Each combination on a new line (space-separated, ascending order).",
        'constraints': "1 <= candidates.length <= 30\n2 <= candidates[i] <= 40\n1 <= target <= 40",
        'examples': [
            {"input": "4 7\n2 3 6 7", "output": "2 2 3\n7", "explanation": "2+2+3=7, and 7=7."},
            {"input": "3 8\n2 3 5", "output": "2 2 2 2\n2 3 3\n3 5", "explanation": "Three combinations sum to 8."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, target;\n"
                "    if (!(cin >> n >> target)) return 0;\n"
                "    vector<int> c(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> c[i];\n"
                "    // Backtracking recursion\n"
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
                "    candidates = sorted([int(x) for x in data[2:2+n]])\n"
                "    res = []\n"
                "    def dfs(remain, start, comb):\n"
                "        if remain == 0:\n"
                "            res.append(list(comb))\n"
                "            return\n"
                "        for i in range(start, n):\n"
                "            if candidates[i] > remain: break\n"
                "            comb.append(candidates[i])\n"
                "            dfs(remain - candidates[i], i, comb)\n"
                "            comb.pop()\n"
                "    dfs(target, 0, [])\n"
                "    for c in res:\n"
                "        print(' '.join(str(x) for x in c))\n\n"
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
                "    const c = tokens.slice(2, 2 + n).map(Number).sort((a, b) => a - b);\n"
                "    const res = [];\n"
                "    function dfs(remain, start, comb) {\n"
                "        if (remain === 0) { res.push([...comb]); return; }\n"
                "        for (let i = start; i < n; i++) {\n"
                "            if (c[i] > remain) break;\n"
                "            comb.push(c[i]);\n"
                "            dfs(remain - c[i], i, comb);\n"
                "            comb.pop();\n"
                "        }\n"
                "    }\n"
                "    dfs(target, 0, []);\n"
                "    for (const row of res) console.log(row.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4 7\n2 3 6 7", 'output': "2 2 3\n7", 'is_sample': True, 'order': 1},
            {'input': "3 8\n2 3 5", 'output': "2 2 2 2\n2 3 3\n3 5", 'is_sample': True, 'order': 2},
            {'input': "1 2\n2", 'output': "2", 'is_sample': False, 'order': 3},
            {'input': "2 1\n2 3", 'output': "", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'letter-combinations-phone-number',
        'title': 'Letter Combinations of Phone Number',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['backtracking', 'strings'],
        'description': (
            "Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number "
            "could represent according to traditional telephone keypads. Print the combinations space-separated in alphabetical order."
        ),
        'input_format': "A single string containing digits `2-9`.",
        'output_format': "Space-separated letter combinations.",
        'constraints': "0 <= digits.length <= 4",
        'examples': [
            {"input": "23", "output": "ad ae af bd be bf cd ce cf", "explanation": "Combinations for '2' (abc) and '3' (def)."},
            {"input": "2", "output": "a b c", "explanation": "'2' maps to a, b, c."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string digits;\n"
                "    if (cin >> digits) {\n"
                "        // Phone keypad backtracking\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    digits = sys.stdin.read().strip()\n"
                "    if not digits:\n"
                "        return\n"
                "    mapping = {'2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}\n"
                "    res = ['']\n"
                "    for d in digits:\n"
                "        res = [prefix + c for prefix in res for c in mapping.get(d, '')]\n"
                "    print(' '.join(res))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const digits = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!digits) return;\n"
                "    const map = { '2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz' };\n"
                "    let res = [''];\n"
                "    for (const d of digits) {\n"
                "        const chars = map[d] || '';\n"
                "        const next = [];\n"
                "        for (const r of res) for (const c of chars) next.push(r + c);\n"
                "        res = next;\n"
                "    }\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "23", 'output': "ad ae af bd be bf cd ce cf", 'is_sample': True, 'order': 1},
            {'input': "2", 'output': "a b c", 'is_sample': True, 'order': 2},
            {'input': "9", 'output': "w x y z", 'is_sample': False, 'order': 3},
            {'input': "79", 'output': "pw px py pz qw qx qy qz rw rx ry rz sw sx sy sz", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'unique-paths',
        'title': 'Unique Paths in a Grid',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming', 'math'],
        'description': (
            "There is a robot on an `m x n` grid. The robot is initially located at the top-left corner `(0, 0)`. "
            "The robot tries to move to the bottom-right corner `(m - 1, n - 1)`. The robot can only move either down or right at any point in time.\n"
            "Given two integers `m` and `n`, return the number of possible unique paths."
        ),
        'input_format': "Two space-separated integers `m` and `n`.",
        'output_format': "The number of unique paths.",
        'constraints': "1 <= m, n <= 100",
        'examples': [
            {"input": "3 7", "output": "28", "explanation": "28 distinct paths on 3x7 grid."},
            {"input": "3 2", "output": "3", "explanation": "Right->Down->Down, Down->Down->Right, Down->Right->Down."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int m, n;\n"
                "    if (cin >> m >> n) {\n"
                "        vector<long long> dp(n, 1);\n"
                "        for (int i = 1; i < m; ++i)\n"
                "            for (int j = 1; j < n; ++j) dp[j] += dp[j - 1];\n"
                "        cout << dp[n - 1] << \"\\n\";\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nimport math\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    m, n = int(data[0]), int(data[1])\n"
                "    print(math.comb(m + n - 2, m - 1))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    const m = parseInt(tokens[0], 10), n = parseInt(tokens[1], 10);\n"
                "    const dp = new Array(n).fill(1);\n"
                "    for (let i = 1; i < m; i++) {\n"
                "        for (let j = 1; j < n; j++) dp[j] += dp[j - 1];\n"
                "    }\n"
                "    console.log(dp[n - 1]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 7", 'output': "28", 'is_sample': True, 'order': 1},
            {'input': "3 2", 'output': "3", 'is_sample': True, 'order': 2},
            {'input': "1 1", 'output': "1", 'is_sample': False, 'order': 3},
            {'input': "5 5", 'output': "70", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'minimum-path-sum',
        'title': 'Minimum Path Sum in Grid',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming', 'matrix'],
        'description': (
            "Given a `m x n` grid filled with non-negative numbers, find a path from top left to bottom right, "
            "which minimizes the sum of all numbers along its path. You can only move down or right."
        ),
        'input_format': "First line contains `m` and `n`.\nThe next `m` lines contain `n` integers each.",
        'output_format': "The minimum path sum.",
        'constraints': "1 <= m, n <= 200\n0 <= grid[i][j] <= 200",
        'examples': [
            {"input": "3 3\n1 3 1\n1 5 1\n4 2 1", "output": "7", "explanation": "Path 1->3->1->1->1 has sum 7."},
            {"input": "2 3\n1 2 3\n4 5 6", "output": "12", "explanation": "Path 1->2->3->6 has sum 12."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int m, n;\n"
                "    if (!(cin >> m >> n)) return 0;\n"
                "    vector<vector<int>> grid(m, vector<int>(n));\n"
                "    for (int i = 0; i < m; ++i)\n"
                "        for (int j = 0; j < n; ++j) cin >> grid[i][j];\n"
                "    // 2D DP\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    m, n = int(data[0]), int(data[1])\n"
                "    grid = []\n"
                "    idx = 2\n"
                "    for _ in range(m):\n"
                "        grid.append([int(x) for x in data[idx:idx+n]])\n"
                "        idx += n\n"
                "    for i in range(m):\n"
                "        for j in range(n):\n"
                "            if i == 0 and j == 0: continue\n"
                "            elif i == 0: grid[i][j] += grid[i][j-1]\n"
                "            elif j == 0: grid[i][j] += grid[i-1][j]\n"
                "            else: grid[i][j] += min(grid[i-1][j], grid[i][j-1])\n"
                "    print(grid[-1][-1])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const m = parseInt(tokens[0], 10), n = parseInt(tokens[1], 10);\n"
                "    const grid = [];\n"
                "    let idx = 2;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        grid.push(tokens.slice(idx, idx + n).map(Number));\n"
                "        idx += n;\n"
                "    }\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        for (let j = 0; j < n; j++) {\n"
                "            if (i === 0 && j === 0) continue;\n"
                "            else if (i === 0) grid[i][j] += grid[i][j - 1];\n"
                "            else if (j === 0) grid[i][j] += grid[i - 1][j];\n"
                "            else grid[i][j] += Math.min(grid[i - 1][j], grid[i][j - 1]);\n"
                "        }\n"
                "    }\n"
                "    console.log(grid[m - 1][n - 1]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 3\n1 3 1\n1 5 1\n4 2 1", 'output': "7", 'is_sample': True, 'order': 1},
            {'input': "2 3\n1 2 3\n4 5 6", 'output': "12", 'is_sample': True, 'order': 2},
            {'input': "1 1\n10", 'output': "10", 'is_sample': False, 'order': 3},
            {'input': "2 2\n1 9\n1 1", 'output': "3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'longest-palindromic-substring',
        'title': 'Longest Palindromic Substring',
        'difficulty': 'medium',
        'challenge_level': 3,
        'xp_reward': 100,
        'tag_slugs': ['strings', 'dynamic-programming', 'two-pointers'],
        'description': (
            "Given a string `s`, return the longest palindromic substring in `s`. "
            "If there are multiple with the same maximum length, return the one that appears earliest."
        ),
        'input_format': "A single line containing the string `s`.",
        'output_format': "The longest palindromic substring.",
        'constraints': "1 <= s.length <= 1000",
        'examples': [
            {"input": "babad", "output": "bab", "explanation": "'bab' (or 'aba') is length 3."},
            {"input": "cbbd", "output": "bb", "explanation": "'bb' is length 2."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s;\n"
                "    if (cin >> s) {\n"
                "        // Expand around center\n"
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
                "    res = ''\n"
                "    for i in range(len(s)):\n"
                "        # Odd length\n"
                "        l, r = i, i\n"
                "        while l >= 0 and r < len(s) and s[l] == s[r]:\n"
                "            if (r - l + 1) > len(res):\n"
                "                res = s[l:r+1]\n"
                "            l -= 1; r += 1\n"
                "        # Even length\n"
                "        l, r = i, i + 1\n"
                "        while l >= 0 and r < len(s) and s[l] == s[r]:\n"
                "            if (r - l + 1) > len(res):\n"
                "                res = s[l:r+1]\n"
                "            l -= 1; r += 1\n"
                "    print(res)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const s = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!s) return;\n"
                "    let res = '';\n"
                "    for (let i = 0; i < s.length; i++) {\n"
                "        let l = i, r = i;\n"
                "        while (l >= 0 && r < s.length && s[l] === s[r]) {\n"
                "            if (r - l + 1 > res.length) res = s.substring(l, r + 1);\n"
                "            l--; r++;\n"
                "        }\n"
                "        l = i; r = i + 1;\n"
                "        while (l >= 0 && r < s.length && s[l] === s[r]) {\n"
                "            if (r - l + 1 > res.length) res = s.substring(l, r + 1);\n"
                "            l--; r++;\n"
                "        }\n"
                "    }\n"
                "    console.log(res);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "babad", 'output': "bab", 'is_sample': True, 'order': 1},
            {'input': "cbbd", 'output': "bb", 'is_sample': True, 'order': 2},
            {'input': "a", 'output': "a", 'is_sample': False, 'order': 3},
            {'input': "racecar", 'output': "racecar", 'is_sample': False, 'order': 4},
        ]
    },
]

