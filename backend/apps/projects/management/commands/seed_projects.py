"""
Management command to seed 6 production guided engineering projects across Python, JavaScript, and C++.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.projects.models import Project, ProjectMilestone


class Command(BaseCommand):
    help = "Seed 6 production guided engineering projects across Python, JavaScript, and C++"

    def handle(self, *args, **options):
        self.stdout.write("Starting Guided Projects Seeder...")

        projects_data = [
            # =========================================================================
            # PYTHON PROJECTS
            # =========================================================================
            {
                "title": "HTTP Request Router & Middleware Engine",
                "slug": "py-http-router",
                "language": "python",
                "difficulty": "medium",
                "challenge_level": 2,
                "short_description": "Build a production-grade HTTP URL router with dynamic path parameters, method dispatching, and chained middleware.",
                "description": """## Overview
Modern web frameworks (Django, FastAPI, Express) rely on high-performance request routers to parse incoming URLs, extract parameterized path segments, and execute middleware chains before invoking handler functions.

In this guided project, you will build a lightweight, production-grade **HTTP Request Router & Middleware Engine** from scratch in pure Python.

### Architectural Goals:
1. Dynamic URL pattern matching with parameter extraction (`/api/v1/users/:user_id/posts/:post_id`).
2. Method-aware request dispatching (GET, POST, PUT, DELETE) with automatic `405 Method Not Allowed` responses.
3. Onion-style middleware pipeline supporting authentication, request timing, and response headers.
""",
                "technologies": ["Python 3", "Regex", "HTTP/1.1", "Middleware Design Pattern"],
                "starter_files": {"router.py": "# Core Router Implementation"},
                "xp_reward": 150,
                "estimated_minutes": 60,
                "order": 1,
                "milestones": [
                    {
                        "order": 1,
                        "title": "Dynamic Path Matching & Parameter Extraction",
                        "description": """Implement `Route` and `match_path(pattern, path)`.
The function should convert URL patterns like `/users/:id/items/:item_id` into regex patterns and return a dictionary of captured parameters.
If the path does not match the pattern, return `None`.

### Example:
```python
match_path('/users/:id', '/users/42') -> {'id': '42'}
match_path('/users/:id', '/orders/42') -> None
```
""",
                        "starter_code": """import re

def match_path(pattern: str, path: str):
    \"\"\"
    Converts :param syntax to regex capture groups and returns extracted params dict.
    Returns None if path does not match pattern.
    \"\"\"
    # Convert pattern like '/users/:id' to regex '^/users/(?P<id>[^/]+)$'
    # TODO: Implement parameter extraction
    pass
""",
                        "test_harness_code": """
# Verification tests
def run_tests():
    # Test 1: Simple exact match
    res1 = match_path('/api/health', '/api/health')
    assert res1 == {}, f"Expected empty dict for exact match, got {res1}"

    # Test 2: Single parameter
    res2 = match_path('/users/:id', '/users/101')
    assert res2 == {'id': '101'}, f"Expected {{'id': '101'}}, got {res2}"

    # Test 3: Multiple parameters
    res3 = match_path('/teams/:team/members/:member', '/teams/alpha/members/john')
    assert res3 == {'team': 'alpha', 'member': 'john'}, f"Expected parameters mismatch: {res3}"

    # Test 4: Mismatch returns None
    res4 = match_path('/users/:id', '/products/101')
    assert res4 is None, f"Expected None for mismatched path, got {res4}"

    print("PASS")

run_tests()
""",
                        "hints": [
                            "Use re.sub to replace `:([a-zA-Z_][a-zA-Z0-9_]*)` with `(?P<\\1>[^/]+)`.",
                            "Remember to wrap the resulting regex with `^` and `$` to prevent partial matches.",
                            "Use match.groupdict() to retrieve captured keyword arguments."
                        ],
                        "xp_reward": 50
                    },
                    {
                        "order": 2,
                        "title": "Method-Aware Route Dispatcher",
                        "description": """Implement `Router` class with `add_route(method, pattern, handler)` and `dispatch(method, path)`.
When matching routes:
- If a route matches both method and path, invoke `handler(params)` and return `(200, result)`.
- If path matches a registered route but method does not match, return `(405, 'Method Not Allowed')`.
- If no route matches the path, return `(404, 'Not Found')`.
""",
                        "starter_code": """import re

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, method: str, pattern: str, handler):
        self.routes.append((method.upper(), pattern, handler))

    def dispatch(self, method: str, path: str):
        # TODO: Implement route matching and dispatching
        pass
""",
                        "test_harness_code": """
def run_tests():
    router = Router()
    router.add_route('GET', '/users/:id', lambda params: f"User {params['id']}")
    router.add_route('POST', '/users', lambda params: "Created User")

    # Test GET match
    s1, r1 = router.dispatch('GET', '/users/42')
    assert s1 == 200 and r1 == "User 42", f"Failed GET match: {s1}, {r1}"

    # Test 405 Method Not Allowed
    s2, r2 = router.dispatch('POST', '/users/42')
    assert s2 == 405, f"Expected 405, got {s2}"

    # Test 404 Not Found
    s3, r3 = router.dispatch('GET', '/non-existent')
    assert s3 == 404, f"Expected 404, got {s3}"

    print("PASS")

run_tests()
""",
                        "hints": [
                            "Track whether the path matched any pattern to distinguish between 404 (no path match) and 405 (path matched but method didn't).",
                            "Convert methods to uppercase using .upper() to ensure case-insensitivity."
                        ],
                        "xp_reward": 50
                    },
                    {
                        "order": 3,
                        "title": "Chained Middleware Pipeline",
                        "description": """Add `use(middleware_fn)` to `Router`.
A middleware function takes `(request_ctx, next_fn)`.
Middleware can inspect/modify `request_ctx`, call `next_fn()`, and inspect/modify the resulting response.
""",
                        "starter_code": """import re

class Router:
    def __init__(self):
        self.routes = []
        self.middlewares = []

    def use(self, middleware):
        self.middlewares.append(middleware)

    def add_route(self, method: str, pattern: str, handler):
        self.routes.append((method.upper(), pattern, handler))

    def dispatch(self, method: str, path: str, ctx=None):
        ctx = ctx or {}
        # TODO: Execute middlewares in order, wrapping the final route handler
        pass
""",
                        "test_harness_code": """
def run_tests():
    router = Router()

    execution_log = []

    def mw1(ctx, next_fn):
        execution_log.append("mw1_pre")
        ctx["auth"] = True
        status, body = next_fn()
        execution_log.append("mw1_post")
        return status, body

    def mw2(ctx, next_fn):
        execution_log.append("mw2_pre")
        status, body = next_fn()
        execution_log.append("mw2_post")
        return status, f"{body}_wrapped"

    router.use(mw1)
    router.use(mw2)
    router.add_route('GET', '/test', lambda params: "Hello")

    status, body = router.dispatch('GET', '/test')
    assert status == 200, f"Expected status 200, got {status}"
    assert body == "Hello_wrapped", f"Expected 'Hello_wrapped', got {body}"
    assert execution_log == ["mw1_pre", "mw2_pre", "mw2_post", "mw1_post"], f"Unexpected execution order: {execution_log}"

    print("PASS")

run_tests()
""",
                        "hints": [
                            "Construct the pipeline from inside out: start with the terminal handler, then wrap it with each middleware in reverse order.",
                            "Each layer should return a callable `lambda: mw(ctx, current_next)`."
                        ],
                        "xp_reward": 50
                    }
                ]
            },

            # =========================================================================
            # PYTHON PROJECT 2: ASYNC TASK QUEUE
            # =========================================================================
            {
                "title": "Persistent Async Task Queue & Worker Daemon",
                "slug": "py-task-queue",
                "language": "python",
                "difficulty": "hard",
                "challenge_level": 3,
                "short_description": "Implement a Celery-like asynchronous task queue with priority scheduling, exponential backoff retries, and dead-letter queues.",
                "description": """## Overview
Background job processing is essential for scalable systems (email sending, image processing, report generation).

In this project, you will build an in-memory **Async Task Queue & Worker Daemon** in Python featuring task registration, priority queueing, retry with exponential backoff, and dead-letter queues.
""",
                "technologies": ["Python 3", "Heapq", "Task Queues", "Fault Tolerance"],
                "starter_files": {"task_queue.py": "# Task Queue Architecture"},
                "xp_reward": 200,
                "estimated_minutes": 75,
                "order": 2,
                "milestones": [
                    {
                        "order": 1,
                        "title": "Task Registration & Priority Queue",
                        "description": """Implement `TaskQueue` with `register(name, fn)`, `enqueue(name, *args, priority=0, **kwargs)`, and `dequeue()`.
Lower priority numbers execute first (priority 0 executes before priority 1).
""",
                        "starter_code": """import heapq
import time
import uuid

class TaskQueue:
    def __init__(self):
        self.registry = {}
        self.queue = []
        self._seq = 0

    def register(self, name: str, fn):
        self.registry[name] = fn

    def enqueue(self, name: str, *args, priority: int = 0, **kwargs):
        # TODO: Push task tuple into heapq
        pass

    def dequeue(self):
        # TODO: Return highest-priority task payload
        pass
""",
                        "test_harness_code": """
def run_tests():
    tq = TaskQueue()
    tq.register('email', lambda to: f"sent to {to}")

    tq.enqueue('email', 'alice@test.com', priority=2)
    tq.enqueue('email', 'boss@test.com', priority=0)
    tq.enqueue('email', 'bob@test.com', priority=1)

    t1 = tq.dequeue()
    t2 = tq.dequeue()
    t3 = tq.dequeue()

    assert t1['args'][0] == 'boss@test.com', f"Expected boss first, got {t1['args'][0]}"
    assert t2['args'][0] == 'bob@test.com', f"Expected bob second, got {t2['args'][0]}"
    assert t3['args'][0] == 'alice@test.com', f"Expected alice third, got {t3['args'][0]}"

    print("PASS")

run_tests()
""",
                        "hints": [
                            "Use `heapq.heappush(self.queue, (priority, self._seq, task_dict))` to ensure stable sorting when priorities match.",
                            "Increment `self._seq` on each enqueue."
                        ],
                        "xp_reward": 60
                    },
                    {
                        "order": 2,
                        "title": "Exponential Backoff & Dead Letter Queue",
                        "description": """Implement `Worker` that executes tasks.
If a task raises an exception:
- Retry up to `max_retries` times with exponential delay calculation: `delay = base_delay * (2 ** retry_count)`.
- If retries are exhausted, move the task to `dead_letter_queue` with status `'FAILED'`.
""",
                        "starter_code": """class Worker:
    def __init__(self, task_queue, max_retries=3, base_delay=1):
        self.tq = task_queue
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.dead_letter_queue = []

    def execute_one(self):
        # TODO: Dequeue task, execute, handle retry or dead-letter queue
        pass
""",
                        "test_harness_code": """
def run_tests():
    tq = TaskQueue()
    attempts = 0

    def flaky_job():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Network glitch")
        return "success"

    tq.register('flaky', flaky_job)
    tq.enqueue('flaky')

    worker = Worker(tq, max_retries=3, base_delay=0)

    # 1st attempt fails, requeues
    r1 = worker.execute_one()
    assert r1['status'] == 'RETRYING', f"Expected RETRYING, got {r1}"

    # 2nd attempt fails, requeues
    r2 = worker.execute_one()
    assert r2['status'] == 'RETRYING'

    # 3rd attempt succeeds
    r3 = worker.execute_one()
    assert r3['status'] == 'SUCCESS', f"Expected SUCCESS, got {r3}"
    assert attempts == 3

    print("PASS")

run_tests()
""",
                        "hints": [
                            "Track `retries` count inside the task dictionary.",
                            "When retries exceed `max_retries`, append to `self.dead_letter_queue` and return `{'status': 'FAILED'}`."
                        ],
                        "xp_reward": 70
                    }
                ]
            },

            # =========================================================================
            # JAVASCRIPT PROJECTS
            # =========================================================================
            {
                "title": "Reactive State Store & Event Bus",
                "slug": "js-state-store",
                "language": "javascript",
                "difficulty": "medium",
                "challenge_level": 2,
                "short_description": "Architect a unidirectional reactive state container like Redux/Zustand with action dispatching, subscriber notification, and memoized selectors.",
                "description": """## Overview
Predictable state management is the cornerstone of modern single-page applications.

In this project, you will build a zero-dependency **Reactive State Store** in JavaScript, featuring:
1. Pure reducer-based state updates.
2. Subscriber listener subscriptions with automatic cleanup.
3. Memoized derived state selectors (`createSelector`).
""",
                "technologies": ["JavaScript (ES2022)", "Functional Programming", "Observer Pattern", "Memoization"],
                "starter_files": {"store.js": "// Reactive Store Implementation"},
                "xp_reward": 150,
                "estimated_minutes": 60,
                "order": 3,
                "milestones": [
                    {
                        "order": 1,
                        "title": "Create Store & Action Dispatcher",
                        "description": """Implement `createStore(reducer, initialState)`.
The store must return:
- `getState()`: Returns current state.
- `dispatch(action)`: Updates state using `reducer(state, action)` and returns action.
- `subscribe(listener)`: Registers listener and returns unsubscribe function.
""",
                        "starter_code": """function createStore(reducer, initialState) {
  let state = initialState;
  const listeners = [];

  return {
    getState: () => state,
    dispatch: (action) => {
      // TODO: Update state using reducer and notify listeners
    },
    subscribe: (listener) => {
      // TODO: Register listener and return unsubscribe function
    }
  };
}
""",
                        "test_harness_code": """
function runTests() {
  const counterReducer = (state = 0, action) => {
    if (action.type === 'INC') return state + (action.payload || 1);
    if (action.type === 'DEC') return state - 1;
    return state;
  };

  const store = createStore(counterReducer, 0);
  let callCount = 0;
  const unsub = store.subscribe(() => { callCount++; });

  store.dispatch({ type: 'INC', payload: 5 });
  if (store.getState() !== 5) throw new Error(`Expected state 5, got ${store.getState()}`);
  if (callCount !== 1) throw new Error(`Expected listener called once, got ${callCount}`);

  unsub();
  store.dispatch({ type: 'DEC' });
  if (store.getState() !== 4) throw new Error(`Expected state 4, got ${store.getState()}`);
  if (callCount !== 1) throw new Error(`Listener called after unsubscribe!`);

  console.log("PASS");
}

runTests();
""",
                        "hints": [
                            "Copy the listeners array during dispatch to prevent issues if a listener unsubscribes during notification.",
                            "Filter or splice the listener from the array in the returned unsubscribe function."
                        ],
                        "xp_reward": 50
                    },
                    {
                        "order": 2,
                        "title": "Memoized Selector Engine",
                        "description": """Implement `createSelector(inputSelectors, transformFn)`.
The selector computes derived state from the store.
If the outputs of `inputSelectors` have not changed (shallow equality `===`), return the previously cached result without re-running `transformFn`.
""",
                        "starter_code": """function createSelector(inputSelectors, transformFn) {
  let lastInputs = null;
  let lastResult = null;

  return function(state) {
    // TODO: Evaluate input selectors, check if changed, compute or return cached
  };
}
""",
                        "test_harness_code": """
function runTests() {
  let computeCount = 0;

  const selectItems = (state) => state.items;
  const selectFilter = (state) => state.filter;

  const selectVisibleItems = createSelector(
    [selectItems, selectFilter],
    (items, filter) => {
      computeCount++;
      return items.filter(item => item.includes(filter));
    }
  );

  const state1 = { items: ['apple', 'banana', 'apricot'], filter: 'ap' };
  const res1 = selectVisibleItems(state1);
  if (res1.length !== 2) throw new Error(`Expected 2 items, got ${res1.length}`);
  if (computeCount !== 1) throw new Error(`Expected computeCount 1, got ${computeCount}`);

  // Re-run with identical state inputs -> Should use cache!
  const res2 = selectVisibleItems(state1);
  if (res2 !== res1) throw new Error(`Expected referential equality for cached result`);
  if (computeCount !== 1) throw new Error(`Expected computeCount to remain 1, got ${computeCount}`);

  // Change filter -> Should recompute
  const state2 = { items: state1.items, filter: 'ban' };
  const res3 = selectVisibleItems(state2);
  if (res3.length !== 1) throw new Error(`Expected 1 item, got ${res3.length}`);
  if (computeCount !== 2) throw new Error(`Expected computeCount 2, got ${computeCount}`);

  console.log("PASS");
}

runTests();
""",
                        "hints": [
                            "Map `inputSelectors` over `state` to get the current input array.",
                            "Compare each input in `currentInputs` against `lastInputs` using `===`.",
                            "Store `lastInputs` and `lastResult` in closure scope."
                        ],
                        "xp_reward": 50
                    }
                ]
            },

            # =========================================================================
            # JAVASCRIPT PROJECT 2: TOKEN BUCKET RATE LIMITER
            # =========================================================================
            {
                "title": "REST API Gateway & Token Bucket Rate Limiter",
                "slug": "js-rate-limiter",
                "language": "javascript",
                "difficulty": "hard",
                "challenge_level": 3,
                "short_description": "Implement a distributed-capable Token Bucket Rate Limiter with burst capacity control, client IP tracking, and HTTP 429 response handling.",
                "description": """## Overview
Rate limiting is a mission-critical component of production API gateways to prevent denial-of-service and brute force attacks.

In this project, you will build an in-memory **Token Bucket Rate Limiter** in JavaScript that handles smooth token refills, burst traffic, and per-client quotas.
""",
                "technologies": ["Node.js", "Token Bucket Algorithm", "API Security", "Concurrency"],
                "starter_files": {"rateLimiter.js": "// Token Bucket Implementation"},
                "xp_reward": 200,
                "estimated_minutes": 75,
                "order": 4,
                "milestones": [
                    {
                        "order": 1,
                        "title": "Token Bucket Core Engine",
                        "description": """Implement `TokenBucket` class with:
- `constructor(capacity, refillRatePerSec)`
- `allowRequest(tokensRequired = 1)`: Refills tokens based on elapsed time since last request (up to capacity). If enough tokens available, deducts them and returns `true`. Otherwise returns `false`.
""",
                        "starter_code": """class TokenBucket {
  constructor(capacity, refillRatePerSec) {
    this.capacity = capacity;
    this.refillRate = refillRatePerSec;
    this.tokens = capacity;
    this.lastRefill = Date.now();
  }

  allowRequest(tokens = 1) {
    // TODO: Calculate elapsed time, add refilled tokens, clamp to capacity, deduct
  }
}
""",
                        "test_harness_code": """
function runTests() {
  const bucket = new TokenBucket(5, 2); // capacity 5, 2 tokens/sec

  // Should allow 5 immediate requests
  for (let i = 0; i < 5; i++) {
    if (!bucket.allowRequest(1)) throw new Error(`Request ${i+1} should be allowed`);
  }

  // 6th request should fail
  if (bucket.allowRequest(1)) throw new Error("Request 6 should be rejected (bucket empty)");

  console.log("PASS");
}

runTests();
""",
                        "hints": [
                            "Elapsed seconds = `(now - this.lastRefill) / 1000`.",
                            "New tokens = `this.tokens + (elapsed * this.refillRate)`.",
                            "Clamp with `Math.min(this.capacity, newTokens)`."
                        ],
                        "xp_reward": 60
                    },
                    {
                        "order": 2,
                        "title": "Per-Client IP Limiter Gateway",
                        "description": """Implement `RateLimitGateway` that manages individual token buckets per client IP address, automatically instantiating buckets on first request.
""",
                        "starter_code": """class RateLimitGateway {
  constructor(capacity, refillRate) {
    this.capacity = capacity;
    this.refillRate = refillRate;
    this.clients = new Map();
  }

  handleRequest(clientIp) {
    // TODO: Retrieve or create bucket for clientIp, return { allowed: boolean, remainingTokens: number }
  }
}
""",
                        "test_harness_code": """
function runTests() {
  const gateway = new RateLimitGateway(2, 1);

  // Client A consumes 2 tokens
  const a1 = gateway.handleRequest('1.1.1.1');
  const a2 = gateway.handleRequest('1.1.1.1');
  const a3 = gateway.handleRequest('1.1.1.1');

  if (!a1.allowed || !a2.allowed) throw new Error("Client A should have 2 allowed requests");
  if (a3.allowed) throw new Error("Client A 3rd request should be blocked");

  // Client B has independent quota
  const b1 = gateway.handleRequest('2.2.2.2');
  if (!b1.allowed) throw new Error("Client B should be allowed independently");

  console.log("PASS");
}

runTests();
""",
                        "hints": [
                            "Use `this.clients.has(ip)` to check if a bucket exists; if not, create `new TokenBucket(this.capacity, this.refillRate)`."
                        ],
                        "xp_reward": 70
                    }
                ]
            },

            # =========================================================================
            # C++ PROJECTS
            # =========================================================================
            {
                "title": "Thread-Safe Memory Pool Allocator",
                "slug": "cpp-memory-pool",
                "language": "cpp",
                "difficulty": "medium",
                "challenge_level": 2,
                "short_description": "Implement a high-performance fixed-size memory pool allocator in modern C++ to eliminate dynamic heap allocation overhead and fragmentation.",
                "description": """## Overview
In high-frequency trading and game engines, dynamic heap allocation (`malloc`/`new`) causes memory fragmentation and unpredictable latency spikes.

In this project, you will build a **Fixed-Size Block Memory Pool Allocator** in modern C++ that achieves $O(1)$ allocation and deallocation using an intrusive free list.
""",
                "technologies": ["C++17", "Memory Management", "Pointers & Offsets", "Systems Programming"],
                "starter_files": {"memory_pool.hpp": "// Memory Pool Header"},
                "xp_reward": 150,
                "estimated_minutes": 60,
                "order": 5,
                "milestones": [
                    {
                        "order": 1,
                        "title": "Slab Partitioning & Intrusive Free List",
                        "description": """Implement `MemoryPool(size_t blockSize, size_t blockCount)` and `allocate()`.
Allocate a contiguous buffer of `blockSize * blockCount` bytes and chain them into an intrusive free list.
`allocate()` pops a block from the free list in $O(1)$ time. If pool is exhausted, return `nullptr`.
""",
                        "starter_code": """#include <iostream>
#include <vector>
#include <cstddef>

class MemoryPool {
private:
    struct Block {
        Block* next;
    };
    size_t blockSize;
    size_t blockCount;
    char* memoryBuffer;
    Block* freeListHead;

public:
    MemoryPool(size_t bSize, size_t bCount) : blockSize(bSize), blockCount(bCount), freeListHead(nullptr) {
        if (blockSize < sizeof(Block*)) blockSize = sizeof(Block*);
        memoryBuffer = new char[blockSize * blockCount];
        // TODO: Chain all blocks into freeListHead
    }

    ~MemoryPool() {
        delete[] memoryBuffer;
    }

    void* allocate() {
        // TODO: Return head of free list, or nullptr if empty
        return nullptr;
    }

    void deallocate(void* ptr) {
        // TODO: Push ptr back onto free list
    }
};
""",
                        "test_harness_code": """
int main() {
    MemoryPool pool(32, 3);

    void* p1 = pool.allocate();
    void* p2 = pool.allocate();
    void* p3 = pool.allocate();
    void* p4 = pool.allocate();

    if (p1 == nullptr || p2 == nullptr || p3 == nullptr) {
        std::cerr << "Failed to allocate 3 blocks\n";
        return 1;
    }
    if (p4 != nullptr) {
        std::cerr << "Pool should return nullptr when exhausted\n";
        return 1;
    }

    pool.deallocate(p2);
    void* p5 = pool.allocate();
    if (p5 != p2) {
        std::cerr << "Recycled block was not reallocated\n";
        return 1;
    }

    std::cout << "PASS\n";
    return 0;
}
""",
                        "hints": [
                            "Cast `memoryBuffer + (i * blockSize)` to `Block*`.",
                            "In `deallocate(void* ptr)`, cast `ptr` to `Block*`, set `block->next = freeListHead`, and `freeListHead = block`."
                        ],
                        "xp_reward": 75
                    }
                ]
            },

            # =========================================================================
            # C++ PROJECT 2: IN-MEMORY KV STORE WITH LRU & WAL
            # =========================================================================
            {
                "title": "In-Memory Key-Value Store with LRU Cache & WAL",
                "slug": "cpp-lru-store",
                "language": "cpp",
                "difficulty": "hard",
                "challenge_level": 3,
                "short_description": "Build a Redis-like in-memory storage engine in C++ featuring an LRU eviction policy, string key-value storage, and write-ahead log recovery.",
                "description": """## Overview
Databases like Redis and SQLite balance microsecond in-memory performance with durability through Write-Ahead Logging (WAL).

In this project, you will construct a **High-Performance In-Memory KV Store** in C++ with $O(1)$ LRU eviction and serialized WAL logging.
""",
                "technologies": ["C++17", "Data Structures", "LRU Eviction", "WAL Persistence"],
                "starter_files": {"kv_store.hpp": "// KV Store Architecture"},
                "xp_reward": 200,
                "estimated_minutes": 75,
                "order": 6,
                "milestones": [
                    {
                        "order": 1,
                        "title": "O(1) LRU Key-Value Cache",
                        "description": """Implement `LRUKVStore` with `get(key)` and `put(key, value)`.
When capacity is exceeded, evict the least recently used key.
""",
                        "starter_code": """#include <iostream>
#include <string>
#include <unordered_map>
#include <list>

class LRUKVStore {
private:
    size_t capacity;
    std::list<std::pair<std::string, std::string>> items;
    std::unordered_map<std::string, std::list<std::pair<std::string, std::string>>::iterator> map;

public:
    LRUKVStore(size_t cap) : capacity(cap) {}

    std::string get(const std::string& key) {
        // TODO: Return value and move key to front; return "" if not found
        return "";
    }

    void put(const std::string& key, const std::string& value) {
        // TODO: Insert/update key and evict least recently used if over capacity
    }
};
""",
                        "test_harness_code": """
int main() {
    LRUKVStore store(2);

    store.put("a", "1");
    store.put("b", "2");

    if (store.get("a") != "1") {
        std::cerr << "Expected 'a' -> '1'\n";
        return 1;
    }

    // Insert 'c' -> should evict 'b' since 'a' was recently accessed
    store.put("c", "3");

    if (store.get("b") != "") {
        std::cerr << "Key 'b' should have been evicted!\n";
        return 1;
    }
    if (store.get("c") != "3" || store.get("a") != "1") {
        std::cerr << "Keys 'a' and 'c' should remain\n";
        return 1;
    }

    std::cout << "PASS\n";
    return 0;
}
""",
                        "hints": [
                            "Use `items.splice(items.begin(), items, it)` to move an accessed item to the front of the list in O(1) time.",
                            "Evict from `items.back()` when `items.size() > capacity`."
                        ],
                        "xp_reward": 80
                    }
                ]
            }
        ]

        with transaction.atomic():
            for pdata in projects_data:
                milestones_data = pdata.pop('milestones', [])
                project, _ = Project.objects.update_or_create(
                    slug=pdata['slug'],
                    defaults=pdata
                )
                self.stdout.write(f"Seeded Project: {project.title} ({project.language})")

                # Reset and seed milestones
                ProjectMilestone.objects.filter(project=project).delete()
                for mdata in milestones_data:
                    ProjectMilestone.objects.create(project=project, **mdata)

        self.stdout.write(self.style.SUCCESS("Successfully seeded 6 Guided Projects and their verification suites!"))

