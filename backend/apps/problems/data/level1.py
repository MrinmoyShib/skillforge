"""
Level 1 Challenges — Apprentice (Syntax & Foundations)
20 foundational challenges designed to build fluency in basic syntax, loops,
arithmetic, conditionals, string operations, and fundamental data structures.
"""

LEVEL_1_CHALLENGES = [
    {
        'base_slug': 'two-sum',
        'title': 'Two Sum',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['hash-table', 'two-pointers', 'arrays'],
        'description': (
            "Given an array of integers `nums` and an integer `target`, return the 0-based indices of the "
            "two numbers such that they add up to `target`.\n\n"
            "You may assume that each input would have **exactly one solution**, and you may not use the "
            "same element twice."
        ),
        'input_format': "First line contains two integers `N` (number of elements) and `target`.\nSecond line contains `N` space-separated integers.",
        'output_format': "Two space-separated indices in ascending order representing the 0-based positions.",
        'constraints': "2 <= N <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9",
        'examples': [
            {"input": "4 9\n2 7 11 15", "output": "0 1", "explanation": "nums[0] + nums[1] = 2 + 7 = 9."},
            {"input": "3 6\n3 2 4", "output": "1 2", "explanation": "nums[1] + nums[2] = 2 + 4 = 6."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <unordered_map>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n, target;\n"
                "    if (!(cin >> n >> target)) return 0;\n"
                "    vector<int> nums(n);\n"
                "    for (int i = 0; i < n; ++i) cin >> nums[i];\n\n"
                "    // Write your solution here\n\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    input_data = sys.stdin.read().split()\n"
                "    if not input_data:\n"
                "        return\n"
                "    n = int(input_data[0])\n"
                "    target = int(input_data[1])\n"
                "    nums = [int(x) for x in input_data[2:2+n]]\n\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 2) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    const target = parseInt(tokens[1], 10);\n"
                "    const nums = tokens.slice(2, 2 + n).map(Number);\n\n"
                "    // Write your solution here\n\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "4 9\n2 7 11 15", 'output': "0 1", 'is_sample': True, 'order': 1},
            {'input': "3 6\n3 2 4", 'output': "1 2", 'is_sample': True, 'order': 2},
            {'input': "2 6\n3 3", 'output': "0 1", 'is_sample': False, 'order': 3},
            {'input': "5 -1\n-5 2 4 8 1", 'output': "0 2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'reverse-string',
        'title': 'Reverse a String',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['strings', 'two-pointers'],
        'description': "Write a program that takes a string `s` and prints it reversed.",
        'input_format': "A single line containing the string `s`.",
        'output_format': "The reversed string on a single line.",
        'constraints': "1 <= s.length <= 10^5\n`s` contains printable characters.",
        'examples': [
            {"input": "hello", "output": "olleh", "explanation": "'hello' reversed is 'olleh'"},
            {"input": "SkillForge", "output": "egroFllikS", "explanation": "'SkillForge' reversed is 'egroFllikS'"}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <algorithm>\n"
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
            {'input': "hello", 'output': "olleh", 'is_sample': True, 'order': 1},
            {'input': "SkillForge", 'output': "egroFllikS", 'is_sample': True, 'order': 2},
            {'input': "a", 'output': "a", 'is_sample': False, 'order': 3},
            {'input': "racecar", 'output': "racecar", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'palindrome-number',
        'title': 'Palindrome Number',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math'],
        'description': "Given an integer `x`, print `true` if `x` is a palindrome, and `false` otherwise. Negative numbers are not palindromes.",
        'input_format': "A single integer `x`.",
        'output_format': "`true` or `false`.",
        'constraints': "-2^31 <= x <= 2^31 - 1",
        'examples': [
            {"input": "121", "output": "true", "explanation": "121 reads the same backward and forward."},
            {"input": "-121", "output": "false", "explanation": "From left to right it is -121. From right to left it is 121-."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    long long x;\n"
                "    if (cin >> x) {\n"
                "        // Write your solution here\n"
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
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const x = parseInt(data, 10);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "121", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "-121", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "10", 'output': "false", 'is_sample': False, 'order': 3},
            {'input': "0", 'output': "true", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'fizz-buzz',
        'title': 'FizzBuzz Sequence',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['loops', 'math'],
        'description': (
            "Given an integer `n`, print the numbers from 1 to `n` separated by spaces. But for multiples of 3, print 'Fizz' "
            "instead of the number, for multiples of 5 print 'Buzz', and for multiples of both 3 and 5 print 'FizzBuzz'."
        ),
        'input_format': "A single integer `n`.",
        'output_format': "A single line containing the space-separated sequence.",
        'constraints': "1 <= n <= 10^4",
        'examples': [
            {"input": "5", "output": "1 2 Fizz 4 Buzz", "explanation": "3 is Fizz, 5 is Buzz."},
            {"input": "15", "output": "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz", "explanation": "15 is divisible by both 3 and 5."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (cin >> n) {\n"
                "        // Write your solution here\n"
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
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5", 'output': "1 2 Fizz 4 Buzz", 'is_sample': True, 'order': 1},
            {'input': "3", 'output': "1 2 Fizz", 'is_sample': True, 'order': 2},
            {'input': "1", 'output': "1", 'is_sample': False, 'order': 3},
            {'input': "15", 'output': "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'valid-parentheses',
        'title': 'Valid Parentheses',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['stack', 'strings'],
        'description': (
            "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', "
            "determine if the input string is valid.\n\n"
            "An input string is valid if open brackets are closed by the same type of brackets in correct order."
        ),
        'input_format': "A single string `s` consisting of parentheses characters.",
        'output_format': "`true` if valid, `false` otherwise.",
        'constraints': "1 <= s.length <= 10^4",
        'examples': [
            {"input": "()[]{}", "output": "true", "explanation": "All bracket pairs match properly."},
            {"input": "(]", "output": "false", "explanation": "Mismatched bracket types."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <stack>\n"
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
            {'input': "()[]{}", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "(]", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "([{}])", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "((((", 'output': "false", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'sum-of-array',
        'title': 'Sum of Array Elements',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'loops'],
        'description': "Given an array of `n` integers, calculate and print the sum of all elements.",
        'input_format': "First line contains `n`. Second line contains `n` integers.",
        'output_format': "A single integer representing the sum.",
        'constraints': "1 <= n <= 10^5\n-10^9 <= a[i] <= 10^9",
        'examples': [
            {"input": "5\n1 2 3 4 5", "output": "15", "explanation": "1 + 2 + 3 + 4 + 5 = 15"},
            {"input": "3\n-10 20 -5", "output": "5", "explanation": "-10 + 20 + -5 = 5"}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    long long sum = 0;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        long long val;\n"
                "        cin >> val;\n"
                "        sum += val;\n"
                "    }\n"
                "    cout << sum << \"\\n\";\n"
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
                "    print(sum(nums))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (tokens.length < 1) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    let sum = 0;\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        sum += parseInt(tokens[i], 10);\n"
                "    }\n"
                "    console.log(sum);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5\n1 2 3 4 5", 'output': "15", 'is_sample': True, 'order': 1},
            {'input': "3\n-10 20 -5", 'output': "5", 'is_sample': True, 'order': 2},
            {'input': "1\n100", 'output': "100", 'is_sample': False, 'order': 3},
            {'input': "4\n0 0 0 0", 'output': "0", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'find-max-min',
        'title': 'Find Maximum and Minimum in Array',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'loops'],
        'description': "Given an array of `n` integers, find the maximum and minimum values in the array.",
        'input_format': "First line contains `n`. Second line contains `n` space-separated integers.",
        'output_format': "Print two space-separated integers: `max min`.",
        'constraints': "1 <= n <= 10^5\n-10^9 <= a[i] <= 10^9",
        'examples': [
            {"input": "5\n3 1 9 4 7", "output": "9 1", "explanation": "Maximum is 9 and minimum is 1."},
            {"input": "3\n-5 -2 -9", "output": "-2 -9", "explanation": "Maximum is -2 and minimum is -9."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <algorithm>\n"
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
            {'input': "5\n3 1 9 4 7", 'output': "9 1", 'is_sample': True, 'order': 1},
            {'input': "3\n-5 -2 -9", 'output': "-2 -9", 'is_sample': True, 'order': 2},
            {'input': "1\n42", 'output': "42 42", 'is_sample': False, 'order': 3},
            {'input': "4\n10 20 30 40", 'output': "40 10", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'count-vowels',
        'title': 'Count Vowels in String',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['strings', 'loops'],
        'description': "Given a string `s`, count the total number of vowels ('a', 'e', 'i', 'o', 'u', case-insensitive).",
        'input_format': "A single line containing the string `s`.",
        'output_format': "A single integer denoting the count of vowels.",
        'constraints': "1 <= s.length <= 10^4",
        'examples': [
            {"input": "developer", "output": "4", "explanation": "Vowels are e, o, e, e (total 4)."},
            {"input": "rhythm", "output": "0", "explanation": "No vowels in 'rhythm'."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
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
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const s = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "developer", 'output': "4", 'is_sample': True, 'order': 1},
            {'input': "rhythm", 'output': "0", 'is_sample': True, 'order': 2},
            {'input': "AEIOUaeiou", 'output': "10", 'is_sample': False, 'order': 3},
            {'input': "SkillForge", 'output': "3", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'factorial',
        'title': 'Factorial of a Number',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math', 'loops'],
        'description': "Given a non-negative integer `n`, compute `n!` (n factorial). Recall that 0! = 1.",
        'input_format': "A single integer `n`.",
        'output_format': "A single integer representing `n!`.",
        'constraints': "0 <= n <= 20",
        'examples': [
            {"input": "5", "output": "120", "explanation": "5! = 5 * 4 * 3 * 2 * 1 = 120"},
            {"input": "0", "output": "1", "explanation": "0! = 1"}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (cin >> n) {\n"
                "        // Write your solution here (use unsigned long long for large values)\n"
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
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5", 'output': "120", 'is_sample': True, 'order': 1},
            {'input': "0", 'output': "1", 'is_sample': True, 'order': 2},
            {'input': "1", 'output': "1", 'is_sample': False, 'order': 3},
            {'input': "10", 'output': "3628800", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'fibonacci-number',
        'title': 'N-th Fibonacci Number',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math', 'dynamic-programming'],
        'description': "The Fibonacci sequence starts F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2) for n >= 2. Given `n`, find F(n).",
        'input_format': "A single integer `n`.",
        'output_format': "The value of F(n).",
        'constraints': "0 <= n <= 30",
        'examples': [
            {"input": "2", "output": "1", "explanation": "F(2) = F(1) + F(0) = 1 + 0 = 1."},
            {"input": "4", "output": "3", "explanation": "F(4) = F(3) + F(2) = 2 + 1 = 3."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (cin >> n) {\n"
                "        // Write your solution here\n"
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
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "2", 'output': "1", 'is_sample': True, 'order': 1},
            {'input': "4", 'output': "3", 'is_sample': True, 'order': 2},
            {'input': "0", 'output': "0", 'is_sample': False, 'order': 3},
            {'input': "10", 'output': "55", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'even-or-odd-count',
        'title': 'Count Even and Odd Numbers',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'loops'],
        'description': "Given an array of `n` integers, count how many numbers are even and how many are odd.",
        'input_format': "First line contains `n`. Second line contains `n` integers.",
        'output_format': "Print two space-separated integers: `even_count odd_count`.",
        'constraints': "1 <= n <= 10^5\n-10^9 <= a[i] <= 10^9",
        'examples': [
            {"input": "5\n1 2 3 4 5", "output": "2 3", "explanation": "2 and 4 are even (2). 1, 3, 5 are odd (3)."},
            {"input": "4\n2 4 6 8", "output": "4 0", "explanation": "All 4 numbers are even."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (!(cin >> n)) return 0;\n"
                "    int even = 0, odd = 0;\n"
                "    for (int i = 0; i < n; ++i) {\n"
                "        int x;\n"
                "        cin >> x;\n"
                "        if (x % 2 == 0) even++;\n"
                "        else odd++;\n"
                "    }\n"
                "    cout << even << \" \" << odd << \"\\n\";\n"
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
                "    even = sum(1 for x in nums if x % 2 == 0)\n"
                "    odd = n - even\n"
                "    print(f\"{even} {odd}\")\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const tokens = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(/\\s+/);\n"
                "    if (!tokens.length) return;\n"
                "    const n = parseInt(tokens[0], 10);\n"
                "    let even = 0, odd = 0;\n"
                "    for (let i = 1; i <= n; i++) {\n"
                "        const x = parseInt(tokens[i], 10);\n"
                "        if (x % 2 === 0) even++;\n"
                "        else odd++;\n"
                "    }\n"
                "    console.log(`${even} ${odd}`);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5\n1 2 3 4 5", 'output': "2 3", 'is_sample': True, 'order': 1},
            {'input': "4\n2 4 6 8", 'output': "4 0", 'is_sample': True, 'order': 2},
            {'input': "3\n1 3 5", 'output': "0 3", 'is_sample': False, 'order': 3},
            {'input': "2\n0 -2", 'output': "2 0", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'multiplication-table',
        'title': 'Multiplication Table',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math', 'loops'],
        'description': "Given an integer `n`, print its multiplication table from `n * 1` to `n * 10` separated by spaces.",
        'input_format': "A single integer `n`.",
        'output_format': "Space-separated products: `n*1 n*2 ... n*10`.",
        'constraints': "1 <= n <= 1000",
        'examples': [
            {"input": "5", "output": "5 10 15 20 25 30 35 40 45 50", "explanation": "5 multiplied by 1 through 10."},
            {"input": "2", "output": "2 4 6 8 10 12 14 16 18 20", "explanation": "2 multiplied by 1 through 10."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int n;\n"
                "    if (cin >> n) {\n"
                "        for (int i = 1; i <= 10; ++i) {\n"
                "            cout << n * i << (i == 10 ? \"\" : \" \");\n"
                "        }\n"
                "        cout << \"\\n\";\n"
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
                "    print(' '.join(str(n * i) for i in range(1, 11)))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    const res = [];\n"
                "    for (let i = 1; i <= 10; i++) res.push(n * i);\n"
                "    console.log(res.join(' '));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "5", 'output': "5 10 15 20 25 30 35 40 45 50", 'is_sample': True, 'order': 1},
            {'input': "2", 'output': "2 4 6 8 10 12 14 16 18 20", 'is_sample': True, 'order': 2},
            {'input': "1", 'output': "1 2 3 4 5 6 7 8 9 10", 'is_sample': False, 'order': 3},
            {'input': "12", 'output': "12 24 36 48 60 72 84 96 108 120", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'leap-year',
        'title': 'Check Leap Year',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math'],
        'description': "Given a year `y`, determine whether it is a leap year. Print `true` if it is, `false` otherwise. (A year is a leap year if divisible by 4, except end-of-century years which must also be divisible by 400).",
        'input_format': "A single integer `y`.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= y <= 9999",
        'examples': [
            {"input": "2024", "output": "true", "explanation": "2024 is divisible by 4 and not a century year."},
            {"input": "1900", "output": "false", "explanation": "1900 is divisible by 100 but not 400."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int y;\n"
                "    if (cin >> y) {\n"
                "        // Write your solution here\n"
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
                "    y = int(data)\n"
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const y = parseInt(data, 10);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "2024", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "1900", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "2000", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "2023", 'output': "false", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'celsius-to-fahrenheit',
        'title': 'Temperature Conversion',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math'],
        'description': "Given a temperature in Celsius `c`, convert it to Fahrenheit using the formula `F = (c * 9/5) + 32`. Print the integer result (rounded down / truncated to integer).",
        'input_format': "A single integer `c`.",
        'output_format': "A single integer representing the temperature in Fahrenheit.",
        'constraints': "-100 <= c <= 100",
        'examples': [
            {"input": "0", "output": "32", "explanation": "0 Celsius = 32 Fahrenheit."},
            {"input": "100", "output": "212", "explanation": "100 Celsius = 212 Fahrenheit."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    int c;\n"
                "    if (cin >> c) {\n"
                "        cout << (c * 9 / 5) + 32 << \"\\n\";\n"
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
                "    c = int(data)\n"
                "    print((c * 9 // 5) + 32)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const c = parseInt(data, 10);\n"
                "    console.log(Math.floor((c * 9) / 5) + 32);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "0", 'output': "32", 'is_sample': True, 'order': 1},
            {'input': "100", 'output': "212", 'is_sample': True, 'order': 2},
            {'input': "25", 'output': "77", 'is_sample': False, 'order': 3},
            {'input': "-40", 'output': "-40", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'check-prime',
        'title': 'Primality Test',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math', 'loops'],
        'description': "Given an integer `n`, determine if it is a prime number. Print `true` if prime, `false` otherwise.",
        'input_format': "A single integer `n`.",
        'output_format': "`true` or `false`.",
        'constraints': "1 <= n <= 10^9",
        'examples': [
            {"input": "7", "output": "true", "explanation": "7 is divisible only by 1 and 7."},
            {"input": "4", "output": "false", "explanation": "4 is divisible by 2."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    long long n;\n"
                "    if (cin >> n) {\n"
                "        // Write your solution here\n"
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
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "7", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "4", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "1", 'output': "false", 'is_sample': False, 'order': 3},
            {'input': "97", 'output': "true", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'power-of-two',
        'title': 'Power of Two',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math'],
        'description': "Given an integer `n`, return `true` if it is a power of two. Otherwise, return `false`.",
        'input_format': "A single integer `n`.",
        'output_format': "`true` or `false`.",
        'constraints': "-2^31 <= n <= 2^31 - 1",
        'examples': [
            {"input": "16", "output": "true", "explanation": "2^4 = 16."},
            {"input": "3", "output": "false", "explanation": "3 is not a power of 2."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    long long n;\n"
                "    if (cin >> n) {\n"
                "        // Write your solution here\n"
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
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "16", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "3", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "1", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "0", 'output': "false", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'string-length',
        'title': 'String Character Count',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['strings'],
        'description': "Given a single word string `s`, output its total character length.",
        'input_format': "A single string `s`.",
        'output_format': "A single integer denoting length.",
        'constraints': "0 <= s.length <= 10^5",
        'examples': [
            {"input": "SkillForge", "output": "10", "explanation": "'SkillForge' has 10 characters."},
            {"input": "code", "output": "4", "explanation": "'code' has 4 characters."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s;\n"
                "    if (cin >> s) cout << s.length() << \"\\n\";\n"
                "    else cout << 0 << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    s = sys.stdin.read().strip()\n"
                "    print(len(s))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const s = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    console.log(s.length);\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "SkillForge", 'output': "10", 'is_sample': True, 'order': 1},
            {'input': "code", 'output': "4", 'is_sample': True, 'order': 2},
            {'input': "a", 'output': "1", 'is_sample': False, 'order': 3},
            {'input': "supercalifragilisticexpialidocious", 'output': "34", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'remove-spaces',
        'title': 'Remove Whitespace from String',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['strings'],
        'description': "Given a line of text, remove all spaces and print the compacted string.",
        'input_format': "A line of text containing spaces.",
        'output_format': "The text with all spaces removed.",
        'constraints': "1 <= text.length <= 10^5",
        'examples': [
            {"input": "hello world from skillforge", "output": "helloworldfromskillforge", "explanation": "Spaces removed."},
            {"input": "a b c d", "output": "abcd", "explanation": "Spaces removed."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string s, word;\n"
                "    while (cin >> word) cout << word;\n"
                "    cout << \"\\n\";\n"
                "    return 0;\n"
                "}\n"
            ),
            'python': (
                "import sys\n\n"
                "def solve():\n"
                "    text = sys.stdin.read()\n"
                "    print(''.join(text.split()))\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const text = fs.readFileSync('/dev/stdin', 'utf-8');\n"
                "    console.log(text.replace(/\\s+/g, ''));\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "hello world from skillforge", 'output': "helloworldfromskillforge", 'is_sample': True, 'order': 1},
            {'input': "a b c d", 'output': "abcd", 'is_sample': True, 'order': 2},
            {'input': "nospaces", 'output': "nospaces", 'is_sample': False, 'order': 3},
            {'input': "  trailing and leading  ", 'output': "trailingandleading", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'second-largest-element',
        'title': 'Second Largest Number in Array',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['arrays', 'loops'],
        'description': "Given an array of `n` integers where there are at least two distinct elements, find the second largest distinct element.",
        'input_format': "First line contains `n`. Second line contains `n` integers.",
        'output_format': "The second largest distinct integer.",
        'constraints': "2 <= n <= 10^5\n-10^9 <= a[i] <= 10^9",
        'examples': [
            {"input": "5\n12 35 1 10 34", "output": "34", "explanation": "Largest is 35, second largest is 34."},
            {"input": "4\n10 10 9 8", "output": "9", "explanation": "Distinct values are 10, 9, 8; second largest is 9."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <set>\n"
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
            {'input': "5\n12 35 1 10 34", 'output': "34", 'is_sample': True, 'order': 1},
            {'input': "4\n10 10 9 8", 'output': "9", 'is_sample': True, 'order': 2},
            {'input': "2\n5 2", 'output': "2", 'is_sample': False, 'order': 3},
            {'input': "5\n-1 -2 -3 -4 -5", 'output': "-2", 'is_sample': False, 'order': 4},
        ]
    },
    {
        'base_slug': 'armstrong-number',
        'title': 'Check Armstrong Number',
        'difficulty': 'easy',
        'challenge_level': 1,
        'xp_reward': 50,
        'tag_slugs': ['math'],
        'description': (
            "An Armstrong number (or narcissistic number) of `k` digits is an integer such that the sum of its "
            "digits each raised to the power of `k` equals the number itself.\n"
            "Given `n`, print `true` if `n` is an Armstrong number, and `false` otherwise."
        ),
        'input_format': "A single integer `n`.",
        'output_format': "`true` or `false`.",
        'constraints': "0 <= n <= 10^7",
        'examples': [
            {"input": "153", "output": "true", "explanation": "1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153."},
            {"input": "123", "output": "false", "explanation": "1^3 + 2^3 + 3^3 = 1 + 8 + 27 = 36 != 123."}
        ],
        'starters': {
            'cpp': (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <cmath>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    long long n;\n"
                "    if (cin >> n) {\n"
                "        // Write your solution here\n"
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
                "    # Write your solution here\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            'javascript': (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const data = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "    if (!data) return;\n"
                "    const n = parseInt(data, 10);\n"
                "    // Write your solution here\n"
                "}\n\n"
                "solve();\n"
            ),
        },
        'test_cases': [
            {'input': "153", 'output': "true", 'is_sample': True, 'order': 1},
            {'input': "123", 'output': "false", 'is_sample': True, 'order': 2},
            {'input': "370", 'output': "true", 'is_sample': False, 'order': 3},
            {'input': "9", 'output': "true", 'is_sample': False, 'order': 4},
        ]
    },
]

