import { useState } from 'react';
import { Link } from 'react-router';
import { useAuth } from '../context/AuthContext';

const CODE_SAMPLES = {
  python: {
    id: 'python',
    name: 'Python 3',
    icon: '🐍',
    filename: 'problem_01_two_sum.py',
    badgeColor: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
    speed: '0.04s',
    code: (
      <>
        <div className="text-slate-500"># Problem: Find two numbers that sum to target value</div>
        <div>
          <span className="text-pink-400">def</span> <span className="text-blue-400">two_sum</span>(nums: <span className="text-indigo-300">list[int]</span>, target: <span className="text-indigo-300">int</span>) -&gt; <span className="text-indigo-300">list[int]</span>:
        </div>
        <div className="pl-4 text-slate-400">lookup = &#123;&#125;</div>
        <div className="pl-4">
          <span className="text-pink-400">for</span> i, num <span className="text-pink-400">in</span> <span className="text-cyan-400">enumerate</span>(nums):
        </div>
        <div className="pl-8 text-slate-400">complement = target - num</div>
        <div className="pl-8">
          <span className="text-pink-400">if</span> complement <span className="text-pink-400">in</span> lookup:
        </div>
        <div className="pl-12 text-emerald-400">
          <span className="text-pink-400">return</span> [lookup[complement], i]
        </div>
        <div className="pl-8 text-slate-400">lookup[num] = i</div>
        <div className="pl-4">
          <span className="text-pink-400">return</span> []
        </div>
      </>
    ),
  },
  javascript: {
    id: 'javascript',
    name: 'JavaScript',
    icon: '🟨',
    filename: 'problem_01_two_sum.js',
    badgeColor: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    speed: '0.03s',
    code: (
      <>
        <div className="text-slate-500">// Problem: Find two numbers that sum to target value</div>
        <div>
          <span className="text-pink-400">function</span> <span className="text-blue-400">twoSum</span>(nums, target) &#123;
        </div>
        <div className="pl-4 text-slate-400">
          <span className="text-pink-400">const</span> lookup = <span className="text-pink-400">new</span> <span className="text-indigo-300">Map</span>();
        </div>
        <div className="pl-4">
          <span className="text-pink-400">for</span> (<span className="text-pink-400">let</span> i = 0; i &lt; nums.length; i++) &#123;
        </div>
        <div className="pl-8 text-slate-400">
          <span className="text-pink-400">const</span> complement = target - nums[i];
        </div>
        <div className="pl-8">
          <span className="text-pink-400">if</span> (lookup.<span className="text-cyan-400">has</span>(complement)) &#123;
        </div>
        <div className="pl-12 text-emerald-400">
          <span className="text-pink-400">return</span> [lookup.<span className="text-cyan-400">get</span>(complement), i];
        </div>
        <div className="pl-8">&#125;</div>
        <div className="pl-8 text-slate-400">lookup.<span className="text-cyan-400">set</span>(nums[i], i);</div>
        <div className="pl-4">&#125;</div>
        <div className="pl-4">
          <span className="text-pink-400">return</span> [];
        </div>
        <div>&#125;</div>
      </>
    ),
  },
  cpp: {
    id: 'cpp',
    name: 'C++',
    icon: '⚡',
    filename: 'problem_01_two_sum.cpp',
    badgeColor: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    speed: '0.01s',
    code: (
      <>
        <div className="text-slate-500">// Problem: Find two numbers that sum to target value</div>
        <div><span className="text-pink-400">#include</span> <span className="text-amber-300">&lt;vector&gt;</span></div>
        <div><span className="text-pink-400">#include</span> <span className="text-amber-300">&lt;unordered_map&gt;</span></div>
        <div className="text-slate-500 mt-1">using namespace std;</div>
        <div className="mt-1"><span className="text-indigo-400">vector&lt;int&gt;</span> <span className="text-blue-400">twoSum</span>(vector&lt;int&gt;&amp; nums, <span className="text-indigo-400">int</span> target) &#123;</div>
        <div className="pl-4 text-slate-400">unordered_map&lt;int, int&gt; lookup;</div>
        <div className="pl-4"><span className="text-pink-400">for</span> (<span className="text-indigo-400">int</span> i = 0; i &lt; nums.size(); ++i) &#123;</div>
        <div className="pl-8 text-slate-400"><span className="text-indigo-400">int</span> complement = target - nums[i];</div>
        <div className="pl-8"><span className="text-pink-400">if</span> (lookup.count(complement)) &#123;</div>
        <div className="pl-12 text-emerald-400"><span className="text-pink-400">return</span> &#123;lookup[complement], i&#125;;</div>
        <div className="pl-8">&#125;</div>
        <div className="pl-8 text-slate-400">lookup[nums[i]] = i;</div>
        <div className="pl-4">&#125;</div>
        <div className="pl-4"><span className="text-pink-400">return</span> &#123;&#125;;</div>
        <div>&#125;</div>
      </>
    ),
  },
};

export default function HomePage() {
  const { user } = useAuth();
  const [activeLang, setActiveLang] = useState('python');

  const currentSample = CODE_SAMPLES[activeLang] || CODE_SAMPLES.python;

  return (
    <div className="space-y-16 sm:space-y-24 py-4 sm:py-6 w-full max-w-full overflow-hidden">
      {/* Hero Section */}
      <section className="relative text-center max-w-4xl mx-auto pt-4 sm:pt-6 pb-8 sm:pb-12 px-2 sm:px-4 overflow-hidden">
        {/* Glow effect in background */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[min(600px,90vw)] h-[350px] bg-indigo-600/15 blur-[90px] sm:blur-[120px] -z-10 rounded-full pointer-events-none" />

        {/* Announcement Pill */}
        <div className="inline-flex items-center gap-2 px-3 sm:px-3.5 py-1.5 rounded-full bg-slate-800/80 border border-slate-700/80 text-xs text-slate-300 mb-6 sm:mb-8 backdrop-blur-md shadow-inner max-w-full">
          <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-ping shrink-0" />
          <span className="font-semibold text-white">SkillForge v1.1</span>
          <span className="hidden sm:inline text-slate-500">•</span>
          <span className="hidden sm:inline">300 Challenges • Python, JavaScript &amp; C++</span>
        </div>

        {/* Main Headline */}
        <h1 className="text-3xl sm:text-5xl md:text-6xl font-black text-white tracking-tight leading-[1.15] mb-6">
          Forge Real Engineering Skills.{' '}
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-cyan-300 to-emerald-400">
            Build Verifiable Proof.
          </span>
        </h1>

        {/* Subtitle */}
        <p className="text-base sm:text-lg md:text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed mb-8 sm:mb-10 px-2">
          Master algorithms and system patterns across <span className="text-white font-medium">Python</span>, <span className="text-white font-medium">JavaScript</span>, and <span className="text-white font-medium">C++</span>. Solve calibrated challenges in isolated sandboxes, build guided engineering projects, and showcase recruiter-ready proof of skill at $0 cost.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-4 px-2">
          {user ? (
            <Link
              to="/dashboard"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-bold text-sm shadow-xl shadow-indigo-500/25 transition transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
            >
              <span>Go to Your Dashboard</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </Link>
          ) : (
            <>
              <Link
                to="/register"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-bold text-sm shadow-xl shadow-indigo-500/25 transition transform hover:-translate-y-0.5 flex items-center justify-center gap-2"
              >
                <span>Start Practicing for Free</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </Link>
              <Link
                to="/login"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-800/90 hover:bg-slate-700/90 border border-slate-700 text-slate-200 hover:text-white font-semibold text-sm transition shadow-sm backdrop-blur-sm text-center"
              >
                Sign In
              </Link>
            </>
          )}
        </div>

        {/* Feature badges row */}
        <div className="mt-8 sm:mt-12 pt-6 sm:pt-8 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 sm:gap-6 text-slate-400 text-xs font-medium">
          <div className="flex items-center justify-center gap-2">
            <span className="text-emerald-400">✓</span> 300 Curated Challenges (3 Tracks)
          </div>
          <div className="flex items-center justify-center gap-2">
            <span className="text-emerald-400">✓</span> Judge0 Isolated Sandboxes
          </div>
          <div className="flex items-center justify-center gap-2">
            <span className="text-emerald-400">✓</span> Anti-Farming XP Engine
          </div>
          <div className="flex items-center justify-center gap-2">
            <span className="text-emerald-400">✓</span> 100% Free &amp; Open Source
          </div>
        </div>
      </section>

      {/* Interactive Code / Mockup Showcase with Multi-Language Switcher */}
      <section className="max-w-5xl mx-auto w-full min-w-0">
        <div className="rounded-2xl border border-slate-800 bg-slate-950/80 shadow-2xl overflow-hidden backdrop-blur-md w-full min-w-0">
          {/* Terminal Window Header with Language Switcher */}
          <div className="px-3 sm:px-4 py-3 bg-slate-900 border-b border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
            <div className="flex items-center gap-3 min-w-0">
              <div className="flex items-center gap-1.5 shrink-0">
                <div className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
                <div className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
              </div>

              {/* Language Selector Tabs */}
              <div className="flex items-center bg-slate-950 p-0.5 rounded-lg border border-slate-800">
                {Object.values(CODE_SAMPLES).map((lang) => (
                  <button
                    key={lang.id}
                    onClick={() => setActiveLang(lang.id)}
                    className={`px-2.5 py-1 text-xs font-medium rounded-md transition flex items-center gap-1.5 ${activeLang === lang.id
                        ? 'bg-slate-800 text-white shadow-sm'
                        : 'text-slate-400 hover:text-slate-200'
                      }`}
                  >
                    <span>{lang.icon}</span>
                    <span>{lang.name}</span>
                  </button>
                ))}
              </div>

              <span className="hidden md:inline text-xs font-mono text-slate-400 truncate">
                {currentSample.filename}
              </span>
            </div>

            <div className="flex items-center gap-2 text-xs shrink-0 self-start sm:self-auto">
              <span className="px-2 py-0.5 rounded bg-emerald-950/80 border border-emerald-800/50 text-emerald-300 font-semibold font-mono text-[11px]">
                Accepted ({currentSample.speed})
              </span>
              <span className="text-indigo-400 font-bold font-mono text-xs">+50 XP</span>
            </div>
          </div>

          {/* Code Body & Evaluation Preview */}
          <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-800 font-mono text-xs min-w-0">
            {/* Editor Code Pane */}
            <div className="md:col-span-2 p-4 sm:p-5 text-slate-300 leading-relaxed overflow-x-auto min-w-0 bg-[#0d1117]">
              {currentSample.code}
            </div>

            {/* Test Case & Progress Outcome */}
            <div className="p-5 bg-slate-900/60 flex flex-col justify-between space-y-4">
              <div>
                <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold mb-3 flex items-center justify-between">
                  <span>Grading Verdict</span>
                  <span className={`px-1.5 py-0.5 rounded text-[10px] border ${currentSample.badgeColor}`}>
                    {currentSample.name} Track
                  </span>
                </div>
                <div className="space-y-2">
                  <div className="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-800/40 text-emerald-300 flex items-center justify-between text-xs">
                    <span>Test Case 1 (Sample)</span>
                    <span className="font-bold">PASSED</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-800/40 text-emerald-300 flex items-center justify-between text-xs">
                    <span>Test Case 2 (Edge Case)</span>
                    <span className="font-bold">PASSED</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-800/40 text-emerald-300 flex items-center justify-between text-xs">
                    <span>Test Case 3 (Large Input)</span>
                    <span className="font-bold">PASSED</span>
                  </div>
                </div>
              </div>

              {/* Progress Toast */}
              <div className="p-3.5 rounded-xl bg-indigo-950/50 border border-indigo-500/30">
                <div className="flex items-center gap-2 text-indigo-300 font-bold text-xs">
                  <span>🎉</span> Problem Mastered!
                </div>
                <p className="text-[11px] text-slate-400 mt-1">
                  Awarded +50 XP on {currentSample.name}. Level progress: 450 / 500 XP to Level 4.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3 Dedicated Language Tracks */}
      <section className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-xs uppercase tracking-widest font-bold text-cyan-400 mb-2">
            Multi-Language Curriculum
          </h2>
          <p className="text-3xl sm:text-4xl font-black text-white">
            Choose Your Preferred Tech Track
          </p>
          <p className="text-slate-400 text-sm mt-2 max-w-xl mx-auto">
            Each track contains 100 progressive problems calibrated from beginner fundamentals to grandmaster system challenges.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Python Track */}
          <div className="p-6 rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 border border-yellow-500/30 shadow-lg hover:border-yellow-400/60 transition group">
            <div className="flex items-center justify-between mb-4">
              <span className="text-3xl">🐍</span>
              <span className="px-2.5 py-1 rounded-full text-xs font-bold font-mono bg-yellow-500/10 text-yellow-400 border border-yellow-500/30">
                100 Problems
              </span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2 group-hover:text-yellow-300 transition">Python 3 Track</h3>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">
              Data structures, algorithms, list comprehensions, generators, and clean idiomatic code. Ideal for backend engineers, data science, and technical interviews.
            </p>
            <div className="text-xs text-slate-400 font-mono space-y-1">
              <div>• Level 1-2: Math, strings, hash tables</div>
              <div>• Level 3-4: DFS/BFS, heaps, intervals</div>
              <div>• Level 5: Dynamic programming, hard graphs</div>
            </div>
          </div>

          {/* JavaScript Track */}
          <div className="p-6 rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 border border-amber-500/30 shadow-lg hover:border-amber-400/60 transition group">
            <div className="flex items-center justify-between mb-4">
              <span className="text-3xl">🟨</span>
              <span className="px-2.5 py-1 rounded-full text-xs font-bold font-mono bg-amber-500/10 text-amber-400 border border-amber-500/30">
                100 Problems
              </span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2 group-hover:text-amber-300 transition">JavaScript Track</h3>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">
              Modern ES6+, functional algorithms, closures, asynchronous logic, and web-oriented data transformations for full-stack and frontend specialists.
            </p>
            <div className="text-xs text-slate-400 font-mono space-y-1">
              <div>• Level 1-2: Array methods, objects, recursion</div>
              <div>• Level 3-4: Sliding window, trees, queues</div>
              <div>• Level 5: Advanced memoization &amp; DP</div>
            </div>
          </div>

          {/* C++ Track */}
          <div className="p-6 rounded-2xl bg-gradient-to-b from-slate-900 to-slate-950 border border-blue-500/30 shadow-lg hover:border-blue-400/60 transition group">
            <div className="flex items-center justify-between mb-4">
              <span className="text-3xl">⚡</span>
              <span className="px-2.5 py-1 rounded-full text-xs font-bold font-mono bg-blue-500/10 text-blue-400 border border-blue-500/30">
                100 Problems
              </span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2 group-hover:text-blue-300 transition">C++ Track</h3>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">
              High-performance systems programming, STL algorithms, memory layouts, pointer manipulation, and competitive programming mastery.
            </p>
            <div className="text-xs text-slate-400 font-mono space-y-1">
              <div>• Level 1-2: Vectors, pointers, fast I/O</div>
              <div>• Level 3-4: Binary search trees, graph theory</div>
              <div>• Level 5: Bitmask DP, shortest paths</div>
            </div>
          </div>
        </div>
      </section>

      {/* Core Platform Pillars */}
      <section className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-xs uppercase tracking-widest font-bold text-cyan-400 mb-2">
            Why SkillForge
          </h2>
          <p className="text-3xl sm:text-4xl font-black text-white">
            Engineered for Real Career Readiness
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Pillar 1 */}
          <div className="p-8 rounded-2xl bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] shadow-lg hover:border-indigo-500/40 transition">
            <div className="w-12 h-12 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-2xl mb-6">
              🛡️
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Isolated Sandbox Execution</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Every code submission compiles and runs in isolated Linux containers using Judge0 CE with strict CPU, wall-clock, and memory limits. Untrusted code is completely prevented from touching the network.
            </p>
          </div>

          {/* Pillar 2 */}
          <div className="p-8 rounded-2xl bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] shadow-lg hover:border-cyan-500/40 transition">
            <div className="w-12 h-12 rounded-xl bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-2xl mb-6">
              🛠️
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Guided Engineering Projects</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Step beyond one-off interview questions. Build multi-milestone backend systems, CLI utilities, and algorithms with in-browser automated test harnesses.
            </p>
          </div>

          {/* Pillar 3 */}
          <div className="p-8 rounded-2xl bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] shadow-lg hover:border-emerald-500/40 transition">
            <div className="w-12 h-12 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-2xl mb-6">
              💼
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Recruiter-Ready Portfolio</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Instantly generate a shareable public portfolio at <code className="text-cyan-300 font-mono text-xs">/portfolio/your_name</code> with verified statistics, solved challenges, and verifiable achievements.
            </p>
          </div>
        </div>
      </section>

      {/* 5-Tier Challenge Roadmap */}
      <section className="max-w-6xl mx-auto rounded-3xl bg-slate-900/60 border border-slate-800 p-5 sm:p-8 md:p-12 w-full overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8 sm:mb-10">
          <div>
            <span className="text-xs uppercase tracking-widest font-bold text-indigo-400">Structured Path</span>
            <h2 className="text-2xl sm:text-3xl font-black text-white mt-1">
              300 Progressive Coding Challenges
            </h2>
          </div>
          <p className="text-sm text-slate-400 max-w-md">
            Difficulty ramps gradually so beginners can start confidently while advanced developers can tackle hard graphs and dynamic programming.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-emerald-400 text-xs font-bold font-mono">Level 1 • 60 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Apprentice</h4>
            <p className="text-xs text-slate-400 mt-2">Variables, I/O, conditionals, arithmetic, basic loops across Python, JS &amp; C++.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-emerald-400 text-xs font-bold font-mono">Level 2 • 60 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Scout</h4>
            <p className="text-xs text-slate-400 mt-2">Two-pointers, hash maps, prefix sums, binary search, basic strings.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-cyan-400 text-xs font-bold font-mono">Level 3 • 60 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Craftsman</h4>
            <p className="text-xs text-slate-400 mt-2">Sliding window, intervals, stacks, queues, backtracking, basic DP.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-indigo-400 text-xs font-bold font-mono">Level 4 • 60 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Architect</h4>
            <p className="text-xs text-slate-400 mt-2">Trees, BST, graph BFS/DFS, topological sort, heaps, LCS.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-amber-400 text-xs font-bold font-mono">Level 5 • 60 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Grandmaster</h4>
            <p className="text-xs text-slate-400 mt-2">Bitmask DP, shortest path algorithms, hard graphs, advanced data structures.</p>
          </div>
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="text-center max-w-3xl mx-auto py-10 sm:py-12 px-4 sm:px-6 rounded-3xl bg-gradient-to-b from-indigo-950/40 to-slate-900 border border-indigo-500/20 w-full overflow-hidden">
        <h2 className="text-2xl sm:text-3xl font-black text-white mb-4">
          Ready to Level Up Your Career?
        </h2>
        <p className="text-sm text-slate-300 mb-8 max-w-xl mx-auto leading-relaxed">
          Create an account in 30 seconds. No credit card, no subscription, 100% free forever.
        </p>
        <Link
          to={user ? "/dashboard" : "/register"}
          className="inline-flex px-8 py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white font-bold text-sm shadow-xl shadow-indigo-500/20 transition transform hover:-translate-y-0.5"
        >
          {user ? "View Your Dashboard" : "Get Started Now"}
        </Link>
      </section>
    </div>
  );
}
