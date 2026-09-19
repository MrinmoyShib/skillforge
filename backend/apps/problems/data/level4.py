"""
Level 4 Challenges — Architect (Advanced Data Structures, Trees, Graphs & Optimization)
20 challenges covering heaps, trees, graph traversals (BFS/DFS), topological sorting,
multidimensional DP (LCS, Edit Distance, Knapsack), and bitwise algorithms.
"""

LEVEL_4_CHALLENGES = [
    {
        'base_slug': 'longest-substring-without-repeating-characters',
        'title': 'Longest Substring Without Repeating Characters',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['sliding-window', 'strings', 'hash-table'],
        'description': (
            "Given a string `s`, find the length of the longest substring without repeating characters."
        ),
        'input_format': "A single line containing the string `s`.",
        'output_format': "The length of the longest substring without repeating characters.",
        'constraints': "0 <= s.length <= 5 * 10^4",
        'examples': [
            {"input": "abcabcbb", "output": "3", "explanation": "The answer is 'abc', with length 3."},
            {"input": "bbbbb", "output": "1", "explanation": "The answer is 'b', with length 1."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s;\n"
                "    if (getline(cin, s)) {\n"
                "        // Sliding window with character index map\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    s = sys.stdin.read().rstrip('\\r\\n')\n"
                "    seen = {}\n"
                "    l = 0\n"
                "    ans = 0\n"
                "    for r, c in enumerate(s):\n"
                "        if c in seen and seen[c] >= l:\n"
                "            l = seen[c] + 1\n"
                "        seen[c] = r\n"
                "        ans = max(ans, r - l + 1)\n"
                "    print(ans)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const s = fs.readFileSync('/dev/stdin', 'utf-8').replace(/[\\r\\n]/g, '');\n"
                "    const seen = new Map();\n"
                "    let l = 0, ans = 0;\n"
                "    for (let r = 0; r < s.length; r++) {\n"
                "        const c = s[r];\n"
                "        if (seen.has(c) && seen.get(c) >= l) {\n"
                "            l = seen.get(c) + 1;\n"
                "        }\n"
                "        seen.set(c, r);\n"
                "        if (r - l + 1 > ans) ans = r - l + 1;\n"
                "    }\n"
                "    console.log(ans);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "abcabcbb", 'output': "3", 'is_sample': True, 'order': 1},
            {'input': "bbbbb", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "pwwkew", 'output': "3", 'is_sample': False, 'order': 3},
            {'input': "", 'output': "0", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'top-k-frequent-elements',
        'title': 'Top K Frequent Elements',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['heap', 'hash-table', 'arrays'],
        'description': (
            "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.\n"
            "Print the elements space-separated in descending order of frequency."
        ),
        'input_format': "First line contains `n` and `k`.\nSecond line contains `n` integers.",
        'output_format': "Space-separated top `k` elements in descending frequency order.",
        'constraints': "1 <= n <= 10^5\n1 <= k <= number of unique elements",
        'examples': [
            {"input": "6 2\n1 1 1 2 2 3", "output": "1 2", "explanation": "1 appears 3 times, 2 appears 2 times."},
            {"input": "1 1\n1", "output": "1", "explanation": "Only one element."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <unordered_map>\n"
                "#include <queue>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, k;\n"
                "    if (!(cin >> n >> k)) return 0;\n"
                "    // Frequency count + min-heap\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nfrom collections import Counter\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n, k = int(data[0]), int(data[1])\n"
                "    nums = [int(x) for x in data[2:2+n]]\n"
                "    counts = Counter(nums)\n"
                "    top = [str(x[0]) for x in counts.most_common(k)]\n"
                "    print(' '.join(top))\n\n"
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
                "    const map = new Map();\n"
                "    for (const x of nums) map.set(x, (map.get(x) || 0) + 1);\n"
                "    const sorted = [...map.entries()].sort((a, b) => b[1] - a[1]);\n"
                "    console.log(sorted.slice(0, k).map(e => e[0]).join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "6 2\n1 1 1 2 2 3", 'output': "1 2", 'is_sample': True, 'order': 1},
            {'input': "1 1\n1", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "4 2\n1 2 2 3", 'output': "2 1", 'is_sample': False, 'order': 3},
            {'input': "5 1\n4 4 4 4 5", 'output': "4", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'kth-largest-element',
        'title': 'Kth Largest Element in Array',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['heap', 'sorting', 'arrays'],
        'description': (
            "Given an integer array `nums` and an integer `k`, return the `k`-th largest element in the array.\n"
            "Note that it is the `k`-th largest element in the sorted order, not the `k`-th distinct element."
        ),
        'input_format': "First line contains `n` and `k`.\nSecond line contains `n` integers.",
        'output_format': "The `k`-th largest element.",
        'constraints': "1 <= k <= n <= 10^5\n-10^4 <= nums[i] <= 10^4",
        'examples': [
            {"input": "6 2\n3 2 1 5 6 4", "output": "5", "explanation": "Sorted: [6, 5, 4, 3, 2, 1], 2nd largest is 5."},
            {"input": "9 4\n3 2 3 1 2 4 5 5 6", "output": "4", "explanation": "4th largest is 4."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <queue>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, k;\n"
                "    if (!(cin >> n >> k)) return 0;\n"
                "    priority_queue<int, vector<int>, greater<int>> min_heap;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        int x; cin >> x;\n"
                "        min_heap.push(x);\n"
                "        if (min_heap.size() > k) min_heap.pop();\n"
                "    }\n"
                "    cout << min_heap.top() << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nimport heapq\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n, k = int(data[0]), int(data[1])\n"
                "    nums = [int(x) for x in data[2:2+n]]\n"
                "    heap = nums[:k]\n"
                "    heapq.heapify(heap)\n"
                "    for x in nums[k:]:\n"
                "        if x > heap[0]:\n"
                "            heapq.heappushpop(heap, x)\n"
                "    print(heap[0])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), k = parseInt(tokens[1], 10);\n"
                "    const nums = tokens.slice(2, 2 + n).map(Number).sort((a, b) => b - a);\n"
                "    console.log(nums[k - 1]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "6 2\n3 2 1 5 6 4", 'output': "5", 'is_sample': True, 'order': 1},
            {'input': "9 4\n3 2 3 1 2 4 5 5 6", 'output': "4", 'is_sample': True, 'order': 2},
            {'input': "1 1\n10", 'output': "10", 'is_sample': False, 'order': 3},
            {'input': "5 5\n1 2 3 4 5", 'output': "1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'find-k-pairs-with-smallest-sums',
        'title': 'Find K Pairs with Smallest Sums',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['heap', 'arrays'],
        'description': (
            "You are given two integer arrays `nums1` and `nums2` sorted in ascending order and an integer `k`.\n"
            "Define a pair `(u, v)` which consists of one element from `nums1` and one from `nums2`.\n"
            "Return the `k` pairs `(u_1, v_1), ..., (u_k, v_k)` with the smallest sums, one pair per line."
        ),
        'input_format': "First line contains `n`, `m`, and `k`.\nSecond line contains `n` integers.\nThird line contains `m` integers.",
        'output_format': "Each pair formatted as `u v` on a new line.",
        'constraints': "1 <= n, m <= 10^4\n1 <= k <= 1000",
        'examples': [
            {"input": "3 3 3\n1 7 11\n2 4 6", "output": "1 2\n1 4\n1 6", "explanation": "Smallest pairs have sums 3, 5, 7."},
            {"input": "2 2 3\n1 2\n3 4", "output": "1 3\n2 3\n1 4", "explanation": "Smallest sums."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <queue>\n"
                "#include <tuple>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, m, k;\n"
                "    if (!(cin >> n >> m >> k)) return 0;\n"
                "    // Min-heap tracking (sum, i, j)\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nimport heapq\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n, m, k = int(data[0]), int(data[1]), int(data[2])\n"
                "    nums1 = [int(x) for x in data[3:3+n]]\n"
                "    nums2 = [int(x) for x in data[3+n:3+n+m]]\n"
                "    heap = []\n"
                "    for i in range(min(n, k)):\n"
                "        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))\n"
                "    count = 0\n"
                "    while heap and count < k:\n"
                "        _, i, j = heapq.heappop(heap)\n"
                "        print(f\"{nums1[i]} {nums2[j]}\")\n"
                "        count += 1\n"
                "        if j + 1 < m:\n"
                "            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), m = parseInt(tokens[1], 10), k = parseInt(tokens[2], 10);\n"
                "    const nums1 = tokens.slice(3, 3 + n).map(Number);\n"
                "    const nums2 = tokens.slice(3 + n, 3 + n + m).map(Number);\n"
                "    const pairs = [];\n"
                "    for (let i = 0; i < Math.min(n, k); i++) {\n"
                "        for (let j = 0; j < Math.min(m, k); j++) {\n"
                "            pairs.push([nums1[i], nums2[j], nums1[i] + nums2[j]]);\n"
                "        }\n"
                "    }\n"
                "    pairs.sort((a, b) => a[2] - b[2]);\n"
                "    for (let i = 0; i < Math.min(k, pairs.length); i++) {\n"
                "        console.log(`${pairs[i][0]} ${pairs[i][1]}`);\n"
                "    }\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 3 3\n1 7 11\n2 4 6", 'output': "1 2\n1 4\n1 6", 'is_sample': True, 'order': 1},
            {'input': "2 2 3\n1 2\n3 4", 'output': "1 3\n2 3\n1 4", 'is_sample': True, 'order': 2},
            {'input': "1 1 1\n1\n2", 'output': "1 2", 'is_sample': False, 'order': 3},
            {'input': "2 1 2\n1 3\n2", 'output': "1 2\n3 2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'binary-tree-inorder-traversal',
        'title': 'Binary Tree Inorder Traversal',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['tree', 'stack'],
        'description': (
            "Given a binary tree represented as an array where child pointers are specified: node 1 is root, "
            "and each line gives `left_child right_child` for node `i` (0 if no child), print the inorder traversal."
        ),
        'input_format': "First line contains `n` (number of nodes).\nThe next `n` lines contain `left right` child indices for node `1` to `n`.",
        'output_format': "Space-separated inorder traversal node indices.",
        'constraints': "1 <= n <= 10^4",
        'examples': [
            {"input": "3\n0 2\n3 0\n0 0", "output": "1 3 2", "explanation": "Node 1 has right child 2, node 2 has left child 3."},
            {"input": "1\n0 0", "output": "1", "explanation": "Single root node."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "void inorder(int u, const vector<pair<int, int>>& tree) {\n"
                "    if (!u) return;\n"
                "    inorder(tree[u].first, tree);\n"
                "    cout << u << \" \";\n"
                "    inorder(tree[u].second, tree);\n"
                "}\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<pair<int, int>> tree(n + 1);\n"
                "    for (int i = 1; i <= n; ++i) cin >> tree[i].first >> tree[i].second;\n"
                "    inorder(1, tree);\n"
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
                "    tree = {}\n"
                "    idx = 1\n"
                "    for i in range(1, n + 1):\n"
                "        tree[i] = (int(data[idx]), int(data[idx+1]))\n"
                "        idx += 2\n"
                "    res = []\n"
                "    def inorder(u):\n"
                "        if u == 0: return\n"
                "        inorder(tree[u][0])\n"
                "        res.append(str(u))\n"
                "        inorder(tree[u][1])\n"
                "    inorder(1)\n"
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
                "    const tree = new Array(n + 1);\n"
                "    let idx = 1;\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        tree[i] = [parseInt(tokens[idx], 10), parseInt(tokens[idx + 1], 10)];\n"
                "        idx += 2;\n"
                "    }\n"
                "    const res = [];\n"
                "    function inorder(u) {\n"
                "        if (u === 0) return;\n"
                "        inorder(tree[u][0]);\n"
                "        res.push(u);\n"
                "        inorder(tree[u][1]);\n"
                "    }\n"
                "    inorder(1);\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n0 2\n3 0\n0 0", 'output': "1 3 2", 'is_sample': True, 'order': 1},
            {'input': "1\n0 0", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "2\n2 0\n0 0", 'output': "2 1", 'is_sample': False, 'order': 3},
            {'input': "3\n2 3\n0 0\n0 0", 'output': "2 1 3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'invert-binary-tree',
        'title': 'Invert Binary Tree',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['tree'],
        'description': (
            "Given a binary tree of `n` nodes with node 1 as root and lines giving `left right` child for each node, "
            "invert the binary tree (swap every left and right child) and print the preorder traversal of the inverted tree."
        ),
        'input_format': "First line contains `n`.\nThe next `n` lines contain `left right` for node `1` to `n`.",
        'output_format': "Space-separated preorder traversal of the inverted tree.",
        'constraints': "1 <= n <= 10^4",
        'examples': [
            {"input": "3\n2 3\n0 0\n0 0", "output": "1 3 2", "explanation": "Left child 2 and right child 3 are swapped."},
            {"input": "1\n0 0", "output": "1", "explanation": "Single node."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "void preorder(int u, const vector<pair<int, int>>& tree) {\n"
                "    if (!u) return;\n"
                "    cout << u << \" \";\n"
                "    preorder(tree[u].second, tree); // inverted: visit original right (now left)\n"
                "    preorder(tree[u].first, tree);  // visit original left\n"
                "}\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<pair<int, int>> tree(n + 1);\n"
                "    for (int i = 1; i <= n; ++i) cin >> tree[i].first >> tree[i].second;\n"
                "    preorder(1, tree);\n"
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
                "    tree = {}\n"
                "    idx = 1\n"
                "    for i in range(1, n + 1):\n"
                "        tree[i] = (int(data[idx]), int(data[idx+1]))\n"
                "        idx += 2\n"
                "    res = []\n"
                "    def preorder(u):\n"
                "        if u == 0: return\n"
                "        res.append(str(u))\n"
                "        preorder(tree[u][1])\n"
                "        preorder(tree[u][0])\n"
                "    preorder(1)\n"
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
                "    const tree = new Array(n + 1);\n"
                "    let idx = 1;\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        tree[i] = [parseInt(tokens[idx], 10), parseInt(tokens[idx + 1], 10)];\n"
                "        idx += 2;\n"
                "    }\n"
                "    const res = [];\n"
                "    function preorder(u) {\n"
                "        if (u === 0) return;\n"
                "        res.push(u);\n"
                "        preorder(tree[u][1]);\n"
                "        preorder(tree[u][0]);\n"
                "    }\n"
                "    preorder(1);\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n2 3\n0 0\n0 0", 'output': "1 3 2", 'is_sample': True, 'order': 1},
            {'input': "1\n0 0", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "2\n2 0\n0 0", 'output': "1 2", 'is_sample': False, 'order': 3},
            {'input': "4\n2 3\n4 0\n0 0\n0 0", 'output': "1 3 2 4", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'maximum-depth-binary-tree',
        'title': 'Maximum Depth of Binary Tree',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['tree', 'recursion'],
        'description': (
            "Given a binary tree of `n` nodes with node 1 as root and lines giving `left right` child for each node, "
            "compute its maximum depth (the number of nodes along the longest path from root down to farthest leaf)."
        ),
        'input_format': "First line contains `n`.\nThe next `n` lines contain `left right` for node `1` to `n`.",
        'output_format': "The maximum depth.",
        'constraints': "1 <= n <= 10^4",
        'examples': [
            {"input": "3\n2 3\n0 0\n0 0", "output": "2", "explanation": "Depth is 2 (root + 1 level)."},
            {"input": "1\n0 0", "output": "1", "explanation": "Root only."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int getDepth(int u, const vector<pair<int, int>>& tree) {\n"
                "    if (!u) return 0;\n"
                "    return 1 + max(getDepth(tree[u].first, tree), getDepth(tree[u].second, tree));\n"
                "}\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    vector<pair<int, int>> tree(n + 1);\n"
                "    for (int i = 1; i <= n; ++i) cin >> tree[i].first >> tree[i].second;\n"
                "    cout << getDepth(1, tree) << \"\\n\";\n"
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
                "    tree = {}\n"
                "    idx = 1\n"
                "    for i in range(1, n + 1):\n"
                "        tree[i] = (int(data[idx]), int(data[idx+1]))\n"
                "        idx += 2\n"
                "    def depth(u):\n"
                "        if u == 0: return 0\n"
                "        return 1 + max(depth(tree[u][0]), depth(tree[u][1]))\n"
                "    print(depth(1))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const tree = new Array(n + 1);\n"
                "    let idx = 1;\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        tree[i] = [parseInt(tokens[idx], 10), parseInt(tokens[idx + 1], 10)];\n"
                "        idx += 2;\n"
                "    }\n"
                "    function depth(u) {\n"
                "        if (u === 0) return 0;\n"
                "        return 1 + Math.max(depth(tree[u][0]), depth(tree[u][1]));\n"
                "    }\n"
                "    console.log(depth(1));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n2 3\n0 0\n0 0", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "1\n0 0", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "4\n2 0\n3 0\n4 0\n0 0", 'output': "4", 'is_sample': False, 'order': 3},
            {'input': "2\n0 2\n0 0", 'output': "2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'validate-binary-search-tree',
        'title': 'Validate Binary Search Tree',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['tree', 'recursion'],
        'description': (
            "Given a binary tree of `n` nodes with node values and child pointers: node 1 is root. "
            "Each line gives `value left_child right_child` for node `i`. Determine if it is a valid Binary Search Tree (BST)."
        ),
        'input_format': "First line contains `n`.\nThe next `n` lines contain `val left right` for nodes 1 to `n`.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= n <= 10^4\n-10^9 <= val <= 10^9",
        'examples': [
            {"input": "3\n2 2 3\n1 0 0\n3 0 0", "output": "true", "explanation": "Left is 1 (<2), right is 3 (>2). Valid BST."},
            {"input": "3\n5 2 3\n1 0 0\n4 0 0", "output": "false", "explanation": "Right child has value 4, but root is 5. Invalid BST."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "struct Node { long long val; int l, r; };\n"
                "vector<Node> tree;\n\n"
                "bool isValidBST(int u, long long minVal, long long maxVal) {\n"
                "    if (!u) return true;\n"
                "    if (tree[u].val <= minVal || tree[u].val >= maxVal) return false;\n"
                "    return isValidBST(tree[u].l, minVal, tree[u].val) && isValidBST(tree[u].r, tree[u].val, maxVal);\n"
                "}\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    tree.resize(n + 1);\n"
                "    for (int i = 1; i <= n; ++i) cin >> tree[i].val >> tree[i].l >> tree[i].r;\n"
                "    cout << (isValidBST(1, -1e18, 1e18) ? \"true\" : \"false\") << \"\\n\";\n"
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
                "    tree = {}\n"
                "    idx = 1\n"
                "    for i in range(1, n + 1):\n"
                "        tree[i] = (int(data[idx]), int(data[idx+1]), int(data[idx+2]))\n"
                "        idx += 3\n"
                "    def validate(u, low, high):\n"
                "        if u == 0: return True\n"
                "        val, l, r = tree[u]\n"
                "        if not (low < val < high): return False\n"
                "        return validate(l, low, val) and validate(r, val, high)\n"
                "    print('true' if validate(1, float('-inf'), float('inf')) else 'false')\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const tree = new Array(n + 1);\n"
                "    let idx = 1;\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        tree[i] = [parseInt(tokens[idx], 10), parseInt(tokens[idx + 1], 10), parseInt(tokens[idx + 2], 10)];\n"
                "        idx += 3;\n"
                "    }\n"
                "    function validate(u, low, high) {\n"
                "        if (u === 0) return true;\n"
                "        const [val, l, r] = tree[u];\n"
                "        if (val <= low || val >= high) return false;\n"
                "        return validate(l, low, val) && validate(r, val, high);\n"
                "    }\n"
                "    console.log(validate(1, -Infinity, Infinity) ? 'true' : 'false');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3\n2 2 3\n1 0 0\n3 0 0", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "3\n5 2 3\n1 0 0\n4 0 0", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "1\n10 0 0", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "3\n2 2 3\n2 0 0\n2 0 0", 'output': "false", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'lowest-common-ancestor',
        'title': 'Lowest Common Ancestor in BST',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['tree', 'binary-search'],
        'description': (
            "Given a Binary Search Tree (BST) of `n` nodes and two node values `p` and `q`, find their Lowest Common Ancestor (LCA) node's value."
        ),
        'input_format': "First line contains `n`, `p`, and `q`.\nThe next `n` lines contain `val left right` for nodes 1 to `n` (node 1 is root).",
        'output_format': "The LCA node value.",
        'constraints': "2 <= n <= 10^4\nAll node values are unique.",
        'examples': [
            {"input": "3 1 3\n2 2 3\n1 0 0\n3 0 0", "output": "2", "explanation": "LCA of 1 and 3 in BST rooted at 2 is 2."},
            {"input": "3 1 2\n2 2 3\n1 0 0\n3 0 0", "output": "2", "explanation": "LCA of 1 and 2 is 2."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "struct Node { int val, l, r; };\n\n"
                "int main() {\n"
                "    int n, p, q;\n"
                "    if (!(cin >> n >> p >> q)) return 0;\n"
                "    vector<Node> tree(n + 1);\n"
                "    for (int i = 1; i <= n; ++i) cin >> tree[i].val >> tree[i].l >> tree[i].r;\n"
                "    int curr = 1;\n"
                "    while (curr) {\n"
                "        if (p < tree[curr].val && q < tree[curr].val) curr = tree[curr].l;\n"
                "        else if (p > tree[curr].val && q > tree[curr].val) curr = tree[curr].r;\n"
                "        else { cout << tree[curr].val << \"\\n\"; break; }\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n, p, q = int(data[0]), int(data[1]), int(data[2])\n"
                "    tree = {}\n"
                "    idx = 3\n"
                "    for i in range(1, n + 1):\n"
                "        tree[i] = (int(data[idx]), int(data[idx+1]), int(data[idx+2]))\n"
                "        idx += 3\n"
                "    curr = 1\n"
                "    while curr:\n"
                "        val, l, r = tree[curr]\n"
                "        if p < val and q < val:\n"
                "            curr = l\n"
                "        elif p > val and q > val:\n"
                "            curr = r\n"
                "        else:\n"
                "            print(val)\n"
                "            break\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), p = parseInt(tokens[1], 10), q = parseInt(tokens[2], 10);\n"
                "    const tree = new Array(n + 1);\n"
                "    let idx = 3;\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        tree[i] = [parseInt(tokens[idx], 10), parseInt(tokens[idx + 1], 10), parseInt(tokens[idx + 2], 10)];\n"
                "        idx += 3;\n"
                "    }\n"
                "    let curr = 1;\n"
                "    while (curr) {\n"
                "        const [val, l, r] = tree[curr];\n"
                "        if (p < val && q < val) curr = l;\n"
                "        else if (p > val && q > val) curr = r;\n"
                "        else { console.log(val); break; }\n"
                "    }\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 1 3\n2 2 3\n1 0 0\n3 0 0", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "3 1 2\n2 2 3\n1 0 0\n3 0 0", 'output': "2", 'is_sample': True, 'order': 2},
            {'input': "5 2 4\n6 2 3\n2 4 5\n8 0 0\n0 0 0\n4 0 0", 'output': "2", 'is_sample': False, 'order': 3},
            {'input': "5 0 8\n6 2 3\n2 4 5\n8 0 0\n0 0 0\n4 0 0", 'output': "6", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'number-of-islands',
        'title': 'Number of Islands (Grid BFS/DFS)',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['graphs', 'matrix', 'recursion'],
        'description': (
            "Given an `m x n` 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands.\n"
            "An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically."
        ),
        'input_format': "First line contains `m` and `n`.\nThe next `m` lines contain `n` characters ('1' or '0').",
        'output_format': "The number of islands.",
        'constraints': "1 <= m, n <= 300",
        'examples': [
            {"input": "4 5\n11110\n11010\n11000\n00000", "output": "1", "explanation": "One single island."},
            {"input": "4 5\n11000\n11000\n00100\n00011", "output": "3", "explanation": "Three disconnected islands."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "using namespace std;\n\n"
                "void dfs(int r, int c, vector<string>& g, int m, int n) {\n"
                "    if (r < 0 || r >= m || c < 0 || c >= n || g[r][c] != '1') return;\n"
                "    g[r][c] = '0';\n"
                "    dfs(r + 1, c, g, m, n);\n"
                "    dfs(r - 1, c, g, m, n);\n"
                "    dfs(r, c + 1, g, m, n);\n"
                "    dfs(r, c - 1, g, m, n);\n"
                "}\n\n"
                "int main() {\n"
                "    int m, n;\n"
                "    if (!(cin >> m >> n)) return 0;\n"
                "    vector<string> g(m);\n"
                "    for (int i = 0; i < m; ++i) cin >> g[i];\n"
                "    int islands = 0;\n"
                "    for (int i = 0; i < m; ++i)\n"
                "        for (int j = 0; j < n; ++j)\n"
                "            if (g[i][j] == '1') { dfs(i, j, g, m, n); islands++; }\n"
                "    cout << islands << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nsys.setrecursionlimit(200000)\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    m, n = int(data[0]), int(data[1])\n"
                "    grid = [list(row) for row in data[2:2+m]]\n"
                "    def dfs(r, c):\n"
                "        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1': return\n"
                "        grid[r][c] = '0'\n"
                "        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)\n"
                "    ans = 0\n"
                "    for i in range(m):\n"
                "        for j in range(n):\n"
                "            if grid[i][j] == '1':\n"
                "                dfs(i, j)\n"
                "                ans += 1\n"
                "    print(ans)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const m = parseInt(tokens[0], 10), n = parseInt(tokens[1], 10);\n"
                "    const grid = tokens.slice(2, 2 + m).map(row => row.split(''));\n"
                "    function dfs(r, c) {\n"
                "        if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] !== '1') return;\n"
                "        grid[r][c] = '0';\n"
                "        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1);\n"
                "    }\n"
                "    let count = 0;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        for (let j = 0; j < n; j++) {\n"
                "            if (grid[i][j] === '1') { dfs(i, j); count++; }\n"
                "        }\n"
                "    }\n"
                "    console.log(count);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4 5\n11110\n11010\n11000\n00000", 'output': "1", 'is_sample': True, 'order': 1},
            {'input': "4 5\n11000\n11000\n00100\n00011", 'output': "3", 'is_sample': True, 'order': 2},
            {'input': "1 1\n0", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "2 2\n10\n01", 'output': "2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'clone-graph',
        'title': 'Graph Traversal Reachability',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['graphs', 'bfs'],
        'description': (
            "Given an undirected graph with `n` vertices (1 to n) and `m` edges, find all vertices reachable "
            "from vertex 1. Output the sorted space-separated reachable vertex numbers."
        ),
        'input_format': "First line contains `n` and `m`.\nThe next `m` lines contain two integers `u` and `v`.",
        'output_format': "Space-separated reachable vertex numbers in ascending order.",
        'constraints': "1 <= n <= 10^5\n0 <= m <= 10^5",
        'examples': [
            {"input": "4 3\n1 2\n2 3\n3 4", "output": "1 2 3 4", "explanation": "All 4 vertices connected in line."},
            {"input": "4 1\n1 2", "output": "1 2", "explanation": "Only vertices 1 and 2 reachable."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <queue>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, m;\n"
                "    if (!(cin >> n >> m)) return 0;\n"
                "    vector<vector<int>> adj(n + 1);\n"
                "    for (int i = 0; i < m; ++i) {\n"
                "        int u, v; cin >> u >> v;\n"
                "        adj[u].push_back(v); adj[v].push_back(u);\n"
                "    }\n"
                "    // BFS from 1\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nfrom collections import deque\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n, m = int(data[0]), int(data[1])\n"
                "    adj = {i: [] for i in range(1, n + 1)}\n"
                "    idx = 2\n"
                "    for _ in range(m):\n"
                "        u, v = int(data[idx]), int(data[idx+1])\n"
                "        adj[u].append(v); adj[v].append(u)\n"
                "        idx += 2\n"
                "    visited = {1}\n"
                "    q = deque([1])\n"
                "    while q:\n"
                "        u = q.popleft()\n"
                "        for v in adj[u]:\n"
                "            if v not in visited:\n"
                "                visited.add(v)\n"
                "                q.append(v)\n"
                "    print(' '.join(str(x) for x in sorted(visited)))\n\n"
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
                "        const u = parseInt(tokens[idx], 10), v = parseInt(tokens[idx + 1], 10);\n"
                "        adj[u].push(v); adj[v].push(u);\n"
                "        idx += 2;\n"
                "    }\n"
                "    const visited = new Set([1]);\n"
                "    const queue = [1];\n"
                "    let head = 0;\n"
                "    while (head < queue.length) {\n"
                "        const u = queue[head++];\n"
                "        for (const v of adj[u]) {\n"
                "            if (!visited.has(v)) {\n"
                "                visited.add(v);\n"
                "                queue.push(v);\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    console.log([...visited].sort((a, b) => a - b).join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4 3\n1 2\n2 3\n3 4", 'output': "1 2 3 4", 'is_sample': True, 'order': 1},
            {'input': "4 1\n1 2", 'output': "1 2", 'is_sample': True, 'order': 2},
            {'input': "1 0", 'output': "1", 'is_sample': False, 'order': 3},
            {'input': "3 0", 'output': "1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'course-schedule',
        'title': 'Course Schedule (Topological Sort)',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['graphs', 'topological-sort'],
        'description': (
            "There are `numCourses` courses labeled from `0` to `numCourses - 1`. You are given `m` prerequisites "
            "where each pair `[a, b]` indicates you must take course `b` first if you want to take course `a`.\n"
            "Return `true` if you can finish all courses (no cycle exists in directed graph), or `false` otherwise."
        ),
        'input_format': "First line contains `numCourses` and `m`.\nThe next `m` lines contain `a` and `b`.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= numCourses <= 10^5\n0 <= m <= 10^5",
        'examples': [
            {"input": "2 1\n1 0", "output": "true", "explanation": "Take course 0 then course 1."},
            {"input": "2 2\n1 0\n0 1", "output": "false", "explanation": "Circular dependency between 0 and 1."}
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
                "    vector<vector<int>> adj(n);\n"
                "    vector<int> indegree(n, 0);\n"
                "    for (int i = 0; i < m; ++i) {\n"
                "        int u, v; cin >> u >> v;\n"
                "        adj[v].push_back(u); indegree[u]++;\n"
                "    }\n"
                "    // Kahn's algorithm\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\nfrom collections import deque\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    n, m = int(data[0]), int(data[1])\n"
                "    adj = {i: [] for i in range(n)}\n"
                "    indegree = [0] * n\n"
                "    idx = 2\n"
                "    for _ in range(m):\n"
                "        u, v = int(data[idx]), int(data[idx+1])\n"
                "        adj[v].append(u)\n"
                "        indegree[u] += 1\n"
                "        idx += 2\n"
                "    q = deque([i for i in range(n) if indegree[i] == 0])\n"
                "    taken = 0\n"
                "    while q:\n"
                "        u = q.popleft()\n"
                "        taken += 1\n"
                "        for v in adj[u]:\n"
                "            indegree[v] -= 1\n"
                "            if indegree[v] == 0:\n"
                "                q.append(v)\n"
                "    print('true' if taken == n else 'false')\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), m = parseInt(tokens[1], 10);\n"
                "    const adj = Array.from({length: n}, () => []);\n"
                "    const indegree = new Array(n).fill(0);\n"
                "    let idx = 2;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        const u = parseInt(tokens[idx], 10), v = parseInt(tokens[idx + 1], 10);\n"
                "        adj[v].push(u);\n"
                "        indegree[u]++;\n"
                "        idx += 2;\n"
                "    }\n"
                "    const q = [];\n"
                "    for (let i = 0; i < n; i++) if (indegree[i] === 0) q.push(i);\n"
                "    let head = 0, taken = 0;\n"
                "    while (head < q.length) {\n"
                "        const u = q[head++];\n"
                "        taken++;\n"
                "        for (const v of adj[u]) {\n"
                "            indegree[v]--;\n"
                "            if (indegree[v] === 0) q.push(v);\n"
                "        }\n"
                "    }\n"
                "    console.log(taken === n ? 'true' : 'false');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "2 1\n1 0", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "2 2\n1 0\n0 1", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "1 0", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "3 3\n0 1\n1 2\n2 0", 'output': "false", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'pacific-atlantic-water-flow',
        'title': 'Pacific Atlantic Water Flow',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['graphs', 'matrix', 'bfs'],
        'description': (
            "Given an `m x n` matrix of non-negative integers representing island heights where water flows "
            "to adjacent cells with equal or lower elevation, Pacific touches top and left borders, Atlantic touches bottom and right borders.\n"
            "Print the count of grid cells from which rain water can flow to both oceans."
        ),
        'input_format': "First line contains `m` and `n`.\nThe next `m` lines contain `n` integers each.",
        'output_format': "The total count of cells that can flow to both oceans.",
        'constraints': "1 <= m, n <= 200\n0 <= heights[r][c] <= 10^5",
        'examples': [
            {"input": "5 5\n1 2 2 3 5\n3 2 3 4 4\n2 4 5 3 1\n6 7 1 4 5\n5 1 1 2 4", "output": "7", "explanation": "7 cells reach both oceans."},
            {"input": "1 1\n1", "output": "1", "explanation": "Single cell touches both."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int m, n;\n"
                "    if (!(cin >> m >> n)) return 0;\n"
                "    // BFS/DFS from ocean borders inward\n"
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
                "    h = []\n"
                "    idx = 2\n"
                "    for _ in range(m):\n"
                "        h.append([int(x) for x in data[idx:idx+n]])\n"
                "        idx += n\n"
                "    pac = set()\n"
                "    atl = set()\n"
                "    def dfs(r, c, visited):\n"
                "        visited.add((r, c))\n"
                "        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:\n"
                "            nr, nc = r + dr, c + dc\n"
                "            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited and h[nr][nc] >= h[r][c]:\n"
                "                dfs(nr, nc, visited)\n"
                "    for i in range(m):\n"
                "        dfs(i, 0, pac); dfs(i, n - 1, atl)\n"
                "    for j in range(n):\n"
                "        dfs(0, j, pac); dfs(m - 1, j, atl)\n"
                "    print(len(pac & atl))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const m = parseInt(tokens[0], 10), n = parseInt(tokens[1], 10);\n"
                "    const h = [];\n"
                "    let idx = 2;\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        h.push(tokens.slice(idx, idx + n).map(Number));\n"
                "        idx += n;\n"
                "    }\n"
                "    const pac = Array.from({length: m}, () => new Array(n).fill(false));\n"
                "    const atl = Array.from({length: m}, () => new Array(n).fill(false));\n"
                "    function dfs(r, c, ocean) {\n"
                "        ocean[r][c] = true;\n"
                "        const dirs = [[-1,0],[1,0],[0,-1],[0,1]];\n"
                "        for (const [dr, dc] of dirs) {\n"
                "            const nr = r + dr, nc = c + dc;\n"
                "            if (nr >= 0 && nr < m && nc >= 0 && nc < n && !ocean[nr][nc] && h[nr][nc] >= h[r][c]) {\n"
                "                dfs(nr, nc, ocean);\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    for (let i = 0; i < m; i++) { dfs(i, 0, pac); dfs(i, n - 1, atl); }\n"
                "    for (let j = 0; j < n; j++) { dfs(0, j, pac); dfs(m - 1, j, atl); }\n"
                "    let count = 0;\n"
                "    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) if (pac[i][j] && atl[i][j]) count++;\n"
                "    console.log(count);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5 5\n1 2 2 3 5\n3 2 3 4 4\n2 4 5 3 1\n6 7 1 4 5\n5 1 1 2 4", 'output': "7", 'is_sample': True, 'order': 1},
            {'input': "1 1\n1", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "2 2\n1 1\n1 1", 'output': "4", 'is_sample': False, 'order': 3},
            {'input': "2 2\n3 1\n1 3", 'output': "2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'word-search',
        'title': 'Word Search in Grid (Backtracking)',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['backtracking', 'matrix'],
        'description': (
            "Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.\n"
            "The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically neighboring)."
        ),
        'input_format': "First line contains `m`, `n`, and the target `word`.\nThe next `m` lines contain `n` characters each.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= m, n <= 10\n1 <= word.length <= 15",
        'examples': [
            {"input": "3 4 ABCCED\nABCE\nSFCS\nADEE", "output": "true", "explanation": "Path A->B->C->C->E->D exists."},
            {"input": "3 4 SEE\nABCE\nSFCS\nADEE", "output": "true", "explanation": "Path S->E->E exists."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int m, n;\n"
                "    string word;\n"
                "    if (!(cin >> m >> n >> word)) return 0;\n"
                "    // Backtracking search\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data:\n"
                "        return\n"
                "    m, n, word = int(data[0]), int(data[1]), data[2]\n"
                "    board = [list(row) for row in data[3:3+m]]\n"
                "    def dfs(r, c, k):\n"
                "        if k == len(word): return True\n"
                "        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]: return False\n"
                "        tmp = board[r][c]\n"
                "        board[r][c] = '#'\n"
                "        res = dfs(r+1,c,k+1) or dfs(r-1,c,k+1) or dfs(r,c+1,k+1) or dfs(r,c-1,k+1)\n"
                "        board[r][c] = tmp\n"
                "        return res\n"
                "    for i in range(m):\n"
                "        for j in range(n):\n"
                "            if dfs(i, j, 0):\n"
                "                print('true')\n"
                "                return\n"
                "    print('false')\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const m = parseInt(tokens[0], 10), n = parseInt(tokens[1], 10), word = tokens[2];\n"
                "    const board = tokens.slice(3, 3 + m).map(r => r.split(''));\n"
                "    function dfs(r, c, k) {\n"
                "        if (k === word.length) return true;\n"
                "        if (r < 0 || r >= m || c < 0 || c >= n || board[r][c] !== word[k]) return false;\n"
                "        const tmp = board[r][c];\n"
                "        board[r][c] = '#';\n"
                "        const found = dfs(r+1, c, k+1) || dfs(r-1, c, k+1) || dfs(r, c+1, k+1) || dfs(r, c-1, k+1);\n"
                "        board[r][c] = tmp;\n"
                "        return found;\n"
                "    }\n"
                "    for (let i = 0; i < m; i++) {\n"
                "        for (let j = 0; j < n; j++) {\n"
                "            if (dfs(i, j, 0)) { console.log('true'); return; }\n"
                "        }\n"
                "    }\n"
                "    console.log('false');\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 4 ABCCED\nABCE\nSFCS\nADEE", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "3 4 SEE\nABCE\nSFCS\nADEE", 'output': "true", 'is_sample': True, 'order': 2},
            {'input': "3 4 ABCB\nABCE\nSFCS\nADEE", 'output': "false", 'is_sample': False, 'order': 3},
            {'input': "1 1 A\nA", 'output': "true", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'longest-common-subsequence',
        'title': 'Longest Common Subsequence (LCS)',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming', 'strings'],
        'description': (
            "Given two strings `text1` and `text2`, return the length of their longest common subsequence. "
            "If there is no common subsequence, return 0."
        ),
        'input_format': "Two space-separated strings `text1` and `text2`.",
        'output_format': "The length of their LCS.",
        'constraints': "1 <= text1.length, text2.length <= 1000",
        'examples': [
            {"input": "abcde ace", "output": "3", "explanation": "The longest common subsequence is 'ace' of length 3."},
            {"input": "abc abc", "output": "3", "explanation": "Identical strings."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s1, s2;\n"
                "    if (cin >> s1 >> s2) {\n"
                "        int m = s1.length(), n = s2.length();\n"
                "        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));\n"
                "        for (int i = 1; i <= m; ++i)\n"
                "            for (int j = 1; j <= n; ++j)\n"
                "                dp[i][j] = (s1[i - 1] == s2[j - 1]) ? dp[i - 1][j - 1] + 1 : max(dp[i - 1][j], dp[i][j - 1]);\n"
                "        cout << dp[m][n] << \"\\n\";\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if len(data) < 2: return\n"
                "    s1, s2 = data[0], data[1]\n"
                "    m, n = len(s1), len(s2)\n"
                "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
                "    for i in range(1, m + 1):\n"
                "        for j in range(1, n + 1):\n"
                "            if s1[i - 1] == s2[j - 1]: dp[i][j] = dp[i - 1][j - 1] + 1\n"
                "            else: dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n"
                "    print(dp[m][n])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    const [s1, s2] = tokens;\n"
                "    const m = s1.length, n = s2.length;\n"
                "    const dp = Array.from({length: m + 1}, () => new Array(n + 1).fill(0));\n"
                "    for (let i = 1; i <= m; i++) {\n"
                "        for (let j = 1; j <= n; j++) {\n"
                "            dp[i][j] = s1[i - 1] === s2[j - 1] ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1]);\n"
                "        }\n"
                "    }\n"
                "    console.log(dp[m][n]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "abcde ace", 'output': "3", 'is_sample': True, 'order': 1},
            {'input': "abc abc", 'output': "3", 'is_sample': True, 'order': 2},
            {'input': "abc def", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "oxcpqrsvwf shmtulskrw", 'output': "2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': '01-knapsack',
        'title': '0/1 Knapsack Problem',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming'],
        'description': (
            "Given `n` items with weights `wt` and values `val`, and a knapsack of capacity `W`, "
            "determine the maximum value you can achieve without exceeding capacity (each item can be taken at most once)."
        ),
        'input_format': "First line contains `n` and `W`.\nSecond line contains `n` integers (`weights`).\nThird line contains `n` integers (`values`).",
        'output_format': "The maximum value.",
        'constraints': "1 <= n <= 1000\n1 <= W <= 2000",
        'examples': [
            {"input": "3 50\n10 20 30\n60 100 120", "output": "220", "explanation": "Take items 2 and 3: wt = 20 + 30 = 50, val = 100 + 120 = 220."},
            {"input": "1 10\n15\n100", "output": "0", "explanation": "Item exceeds capacity."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, W;\n"
                "    if (!(cin >> n >> W)) return 0;\n"
                "    vector<int> wt(n), val(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> wt[i];\n"
                "    for (int i = 0; i < n; ++i) cin >> val[i];\n"
                "    vector<int> dp(W + 1, 0);\n"
                "    for (int i = 0; i < n; ++i)\n"
                "        for (int w = W; w >= wt[i]; --w)\n"
                "            dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);\n"
                "    cout << dp[W] << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n, W = int(data[0]), int(data[1])\n"
                "    wt = [int(x) for x in data[2:2+n]]\n"
                "    val = [int(x) for x in data[2+n:2+2*n]]\n"
                "    dp = [0] * (W + 1)\n"
                "    for i in range(n):\n"
                "        for w in range(W, wt[i] - 1, -1):\n"
                "            dp[w] = max(dp[w], dp[w - wt[i]] + val[i])\n"
                "    print(dp[W])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10), W = parseInt(tokens[1], 10);\n"
                "    const wt = tokens.slice(2, 2 + n).map(Number);\n"
                "    const val = tokens.slice(2 + n, 2 + 2 * n).map(Number);\n"
                "    const dp = new Array(W + 1).fill(0);\n"
                "    for (let i = 0; i < n; i++) {\n"
                "        for (let w = W; w >= wt[i]; w--) {\n"
                "            if (dp[w - wt[i]] + val[i] > dp[w]) dp[w] = dp[w - wt[i]] + val[i];\n"
                "        }\n"
                "    }\n"
                "    console.log(dp[W]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "3 50\n10 20 30\n60 100 120", 'output': "220", 'is_sample': True, 'order': 1},
            {'input': "1 10\n15\n100", 'output': "0", 'is_sample': True, 'order': 2},
            {'input': "4 7\n1 3 4 5\n1 4 5 7", 'output': "9", 'is_sample': False, 'order': 3},
            {'input': "2 3\n4 5\n1 2", 'output': "0", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'edit-distance',
        'title': 'Edit Distance (Levenshtein Distance)',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming', 'strings'],
        'description': (
            "Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.\n"
            "Allowed operations are: Insert a character, Delete a character, Replace a character."
        ),
        'input_format': "Two space-separated strings `word1` and `word2`.",
        'output_format': "The minimum edit distance.",
        'constraints': "0 <= word1.length, word2.length <= 500",
        'examples': [
            {"input": "horse ros", "output": "3", "explanation": "horse -> rorse -> rose -> ros."},
            {"input": "intention execution", "output": "5", "explanation": "5 operations needed."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string w1, w2;\n"
                "    if (cin >> w1 >> w2) {\n"
                "        // Levenshtein DP\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if len(data) < 2: return\n"
                "    w1, w2 = data[0], data[1]\n"
                "    m, n = len(w1), len(w2)\n"
                "    dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
                "    for i in range(m + 1): dp[i][0] = i\n"
                "    for j in range(n + 1): dp[0][j] = j\n"
                "    for i in range(1, m + 1):\n"
                "        for j in range(1, n + 1):\n"
                "            if w1[i - 1] == w2[j - 1]: dp[i][j] = dp[i - 1][j - 1]\n"
                "            else: dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n"
                "    print(dp[m][n])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    const [w1, w2] = tokens;\n"
                "    const m = w1.length, n = w2.length;\n"
                "    const dp = Array.from({length: m + 1}, () => new Array(n + 1).fill(0));\n"
                "    for (let i = 0; i <= m; i++) dp[i][0] = i;\n"
                "    for (let j = 0; j <= n; j++) dp[0][j] = j;\n"
                "    for (let i = 1; i <= m; i++) {\n"
                "        for (let j = 1; j <= n; j++) {\n"
                "            dp[i][j] = w1[i - 1] === w2[j - 1] ? dp[i - 1][j - 1] : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);\n"
                "        }\n"
                "    }\n"
                "    console.log(dp[m][n]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "horse ros", 'output': "3", 'is_sample': True, 'order': 1},
            {'input': "intention execution", 'output': "5", 'is_sample': True, 'order': 2},
            {'input': "a a", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "abc def", 'output': "3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'decode-ways',
        'title': 'Decode Ways',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['dynamic-programming', 'strings'],
        'description': (
            "A message containing letters from A-Z can be encoded into numbers using mapping 'A' -> 1, ..., 'Z' -> 26.\n"
            "Given a string `s` containing only digits, return the number of ways to decode it."
        ),
        'input_format': "A single digit string `s`.",
        'output_format': "The number of decoding ways.",
        'constraints': "1 <= s.length <= 100",
        'examples': [
            {"input": "12", "output": "2", "explanation": "'12' could be 'AB' (1 2) or 'L' (12)."},
            {"input": "226", "output": "3", "explanation": "'BZ' (2 26), 'VF' (22 6), or 'BBF' (2 2 6)."}
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
                "        int n = s.length();\n"
                "        vector<long long> dp(n + 1, 0);\n"
                "        dp[0] = 1;\n"
                "        dp[1] = (s[0] != '0');\n"
                "        for (int i = 2; i <= n; ++i) {\n"
                "            int one = s[i - 1] - '0';\n"
                "            int two = stoi(s.substr(i - 2, 2));\n"
                "            if (one >= 1) dp[i] += dp[i - 1];\n"
                "            if (two >= 10 && two <= 26) dp[i] += dp[i - 2];\n"
                "        }\n"
                "        cout << dp[n] << \"\\n\";\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    s = sys.stdin.read().strip()\n"
                "    if not s or s[0] == '0':\n"
                "        print(0); return\n"
                "    n = len(s)\n"
                "    dp = [0] * (n + 1)\n"
                "    dp[0] = 1\n"
                "    dp[1] = 1\n"
                "    for i in range(2, n + 1):\n"
                "        one = int(s[i - 1])\n"
                "        two = int(s[i - 2:i])\n"
                "        if one >= 1: dp[i] += dp[i - 1]\n"
                "        if 10 <= two <= 26: dp[i] += dp[i - 2]\n"
                "    print(dp[n])\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const s = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!s || s[0] === '0') { console.log(0); return; }\n"
                "    const n = s.length;\n"
                "    const dp = new Array(n + 1).fill(0);\n"
                "    dp[0] = 1; dp[1] = 1;\n"
                "    for (let i = 2; i <= n; i++) {\n"
                "        const one = parseInt(s[i - 1], 10);\n"
                "        const two = parseInt(s.substring(i - 2, i), 10);\n"
                "        if (one >= 1) dp[i] += dp[i - 1];\n"
                "        if (two >= 10 && two <= 26) dp[i] += dp[i - 2];\n"
                "    }\n"
                "    console.log(dp[n]);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "12", 'output': "2", 'is_sample': True, 'order': 1},
            {'input': "226", 'output': "3", 'is_sample': True, 'order': 2},
            {'input': "06", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "10", 'output': "1", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'bitwise-and-numbers-range',
        'title': 'Bitwise AND of Numbers Range',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['math'],
        'description': (
            "Given two integers `left` and `right` that represent the range `[left, right]`, "
            "return the bitwise AND of all numbers in this range, inclusive."
        ),
        'input_format': "Two space-separated integers `left` and `right`.",
        'output_format': "The bitwise AND result.",
        'constraints': "0 <= left <= right <= 2^31 - 1",
        'examples': [
            {"input": "5 7", "output": "4", "explanation": "5 & 6 & 7 = 4."},
            {"input": "0 0", "output": "0", "explanation": "0"}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    long long l, r;\n"
                "    if (cin >> l >> r) {\n"
                "        while (r > l) r &= (r - 1);\n"
                "        cout << r << \"\\n\";\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if len(data) < 2: return\n"
                "    l, r = int(data[0]), int(data[1])\n"
                "    while r > l:\n"
                "        r &= (r - 1)\n"
                "    print(r)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    let l = BigInt(tokens[0]), r = BigInt(tokens[1]);\n"
                "    while (r > l) r = r & (r - 1n);\n"
                "    console.log(r.toString());\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5 7", 'output': "4", 'is_sample': True, 'order': 1},
            {'input': "0 0", 'output': "0", 'is_sample': True, 'order': 2},
            {'input': "1 2147483647", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "12 15", 'output': "12", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'single-number-ii',
        'title': 'Single Number II (Thrice Repeated Elements)',
        'difficulty': 'medium',
        'challenge_level': 4,
        'xp_reward': 100,
        'tag_slugs': ['math', 'arrays'],
        'description': (
            "Given an integer array `nums` where every element appears three times except for one, which appears exactly once. "
            "Find the single element and return it in O(n) time and O(1) space."
        ),
        'input_format': "First line contains `n`.\nSecond line contains `n` integers.",
        'output_format': "The unique element.",
        'constraints': "1 <= n <= 3 * 10^4\n-2^31 <= nums[i] <= 2^31 - 1",
        'examples': [
            {"input": "4\n2 2 3 2", "output": "3", "explanation": "2 appears 3 times, 3 appears once."},
            {"input": "7\n0 1 0 1 0 1 99", "output": "99", "explanation": "99 appears once."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    int ones = 0, twos = 0;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        int x; cin >> x;\n"
                "        ones = (ones ^ x) & ~twos;\n"
                "        twos = (twos ^ x) & ~ones;\n"
                "    }\n"
                "    cout << ones << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    data = sys.stdin.read().split()\n"
                "    if not data: return\n"
                "    n = int(data[0])\n"
                "    nums = [int(x) for x in data[1:1+n]]\n"
                "    ones, twos = 0, 0\n"
                "    for x in nums:\n"
                "        ones = (ones ^ x) & ~twos\n"
                "        twos = (twos ^ x) & ~ones\n"
                "    print(ones)\n\n"
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
                "    let ones = 0, twos = 0;\n"
                "    for (const x of nums) {\n"
                "        ones = (ones ^ x) & ~twos;\n"
                "        twos = (twos ^ x) & ~ones;\n"
                "    }\n"
                "    console.log(ones);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4\n2 2 3 2", 'output': "3", 'is_sample': True, 'order': 1},
            {'input': "7\n0 1 0 1 0 1 99", 'output': "99", 'is_sample': True, 'order': 2},
            {'input': "1\n50", 'output': "50", 'is_sample': False, 'order': 3},
            {'input': "4\n-2 -2 100 -2", 'output': "100", 'is_sample': False, 'order': 4},
        ]
    },
]

