import { Link } from 'react-router';
import { useAuth } from '../context/AuthContext';

export default function HomePage() {
  const { user } = useAuth();

  return (
    <div className="space-y-16 sm:space-y-24 py-4 sm:py-6 w-full max-w-full overflow-hidden">
      {/* Hero Section */}
      <section className="relative text-center max-w-4xl mx-auto pt-4 sm:pt-6 pb-8 sm:pb-12 px-2 sm:px-4 overflow-hidden">
        {/* Glow effect in background */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[min(600px,90vw)] h-[350px] bg-indigo-600/15 blur-[90px] sm:blur-[120px] -z-10 rounded-full pointer-events-none" />

        {/* Announcement Pill */}
        <div className="inline-flex items-center gap-2 px-3 sm:px-3.5 py-1.5 rounded-full bg-slate-800/80 border border-slate-700/80 text-xs text-slate-300 mb-6 sm:mb-8 backdrop-blur-md shadow-inner max-w-full">
          <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-ping shrink-0" />
          <span className="font-semibold text-white">SkillForge v1.0</span>
          <span className="hidden sm:inline text-slate-500">•</span>
          <span className="hidden sm:inline">Full-Stack Developer Growth Platform</span>
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
          Not just another LeetCode clone. Solve calibrated C++ challenges in sandboxed environments, earn evidence-based skill ratings, and build a recruiter-ready portfolio at $0 cost.
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
            <span className="text-emerald-400">✓</span> 55 Calibrated Challenges
          </div>
          <div className="flex items-center justify-center gap-2">
            <span className="text-emerald-400">✓</span> Isolated Sandbox Runner
          </div>
          <div className="flex items-center justify-center gap-2">
            <span className="text-emerald-400">✓</span> Anti-Farming XP Engine
          </div>
          <div className="flex items-center justify-center gap-2">
            <span className="text-emerald-400">✓</span> 100% Free & Open Source
          </div>
        </div>
      </section>

      {/* Interactive Code / Mockup Showcase */}
      <section className="max-w-5xl mx-auto w-full min-w-0">
        <div className="rounded-2xl border border-slate-800 bg-slate-950/80 shadow-2xl overflow-hidden backdrop-blur-md w-full min-w-0">
          {/* Terminal Window Header */}
          <div className="px-3 sm:px-4 py-3 bg-slate-900 border-b border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
            <div className="flex items-center gap-2 min-w-0">
              <div className="flex items-center gap-1.5 shrink-0">
                <div className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
                <div className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
              </div>
              <span className="text-xs font-mono text-slate-300 truncate">
                problem_01_two_sum.cpp
              </span>
              <span className="hidden sm:inline text-xs font-mono text-slate-500">— Level 1: Beginner</span>
            </div>
            <div className="flex items-center gap-2 text-xs shrink-0 self-start sm:self-auto">
              <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-semibold font-mono text-[11px]">
                Accepted (0.02s)
              </span>
              <span className="text-indigo-400 font-bold font-mono text-xs">+50 XP</span>
            </div>
          </div>

          {/* Code Body & Evaluation Preview */}
          <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-800 font-mono text-xs min-w-0">
            {/* Editor Code Pane */}
            <div className="md:col-span-2 p-4 sm:p-5 text-slate-300 leading-relaxed overflow-x-auto min-w-0 bg-[#0d1117]">
              <div className="text-slate-500">// Problem: Find two numbers that sum to target value</div>
              <div><span className="text-pink-400">#include</span> <span className="text-amber-300">&lt;iostream&gt;</span></div>
              <div><span className="text-pink-400">#include</span> <span className="text-amber-300">&lt;vector&gt;</span></div>
              <div><span className="text-pink-400">#include</span> <span className="text-amber-300">&lt;unordered_map&gt;</span></div>
              <div className="text-slate-500 mt-2">using namespace std;</div>
              <div className="mt-2"><span className="text-indigo-400">vector&lt;int&gt;</span> <span className="text-blue-400">twoSum</span>(vector&lt;int&gt;&amp; nums, <span className="text-indigo-400">int</span> target) &#123;</div>
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
            </div>

            {/* Test Case & Progress Outcome */}
            <div className="p-5 bg-slate-900/60 flex flex-col justify-between space-y-4">
              <div>
                <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold mb-3">
                  Grading Verdict
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
                  Awarded +50 XP. Level progress: 450 / 500 XP to Level 4.
                </p>
              </div>
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
              Every code submission compiles and runs in isolated Linux containers with strict CPU, wall-clock, and memory limits. Untrusted code is completely prevented from touching the network.
            </p>
          </div>

          {/* Pillar 2 */}
          <div className="p-8 rounded-2xl bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] shadow-lg hover:border-cyan-500/40 transition">
            <div className="w-12 h-12 rounded-xl bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-2xl mb-6">
              📊
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Evidence-Based Skill Trees</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              No hollow self-ratings. Your skills in C++, Algorithms, and Data Structures are dynamically computed and verified by your solved problems and difficulty ratings.
            </p>
          </div>

          {/* Pillar 3 */}
          <div className="p-8 rounded-2xl bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] shadow-lg hover:border-emerald-500/40 transition">
            <div className="w-12 h-12 rounded-xl bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-2xl mb-6">
              💼
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Recruiter-Ready Portfolio</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Instantly generate a shareable public portfolio at <code className="text-cyan-300 font-mono text-xs">/portfolio/your_name</code> with verified statistics, projects, and achievements.
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
              55 Progressive C++ Coding Challenges
            </h2>
          </div>
          <p className="text-sm text-slate-400 max-w-md">
            Difficulty ramps gradually so beginners can start confidently while advanced developers can tackle hard graphs and DP.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-emerald-400 text-xs font-bold font-mono">Level 1 • 10 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Beginner</h4>
            <p className="text-xs text-slate-400 mt-2">Variables, I/O, conditionals, arithmetic, basic loops.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-emerald-400 text-xs font-bold font-mono">Level 2 • 10 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Basic</h4>
            <p className="text-xs text-slate-400 mt-2">Nested loops, functions, arrays, strings, basic logic.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-cyan-400 text-xs font-bold font-mono">Level 3 • 15 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Intermediate</h4>
            <p className="text-xs text-slate-400 mt-2">Two pointers, prefix sums, frequency counting, recursion.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-indigo-400 text-xs font-bold font-mono">Level 4 • 12 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Advanced</h4>
            <p className="text-xs text-slate-400 mt-2">Linked lists, stacks, queues, binary search, trees.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-amber-400 text-xs font-bold font-mono">Level 5 • 8 Problems</span>
            <h4 className="text-base font-bold text-white mt-2">Expert</h4>
            <p className="text-xs text-slate-400 mt-2">Graph algorithms, dynamic programming, hard structures.</p>
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
