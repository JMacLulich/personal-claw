---
phase: 01-foundation-security
plan: 02
subsystem: discord
tags: [discord, py-cord, authentication, authorization, testing, pytest]

# Dependency graph
requires:
  - phase: 01-01
    provides: "Python foundation with configuration system"
provides:
  - "Discord bot with global user allowlist enforcement"
  - "Auth check function validating user IDs against config"
  - "Test suite for allowlist logic"
  - "ping command for authorization testing"
affects: [01-03, 01-04, discord, bot-commands]

# Tech tracking
tech-stack:
  added: [pytest 9.0.2, audioop-lts 0.2.2]
  patterns: [global @bot.check decorator, fail-closed authorization, deferred bot creation]

key-files:
  created:
    - src/auth.py
    - src/bot.py
    - tests/__init__.py
    - tests/test_auth.py
  modified:
    - requirements.txt

key-decisions:
  - "Use @bot.check decorator for global enforcement (security-first, no bypass possible)"
  - "Defer bot creation to runtime to avoid Python 3.14 asyncio event loop issues"
  - "Add audioop-lts for Python 3.13+ compatibility with py-cord"
  - "Test auth logic independently via mocks (no live bot connection required)"

patterns-established:
  - "Global authorization check runs before ALL commands"
  - "Fail-closed security: unauthorized users rejected by default"
  - "User-friendly error messages for rejected commands"
  - "Deferred resource initialization to avoid import-time issues"

# Metrics
duration: 3min
completed: 2026-02-03
---

# Phase 01 Plan 02: Discord Bot with User Allowlist Summary

**Discord bot with global @bot.check authorization enforcing single-user access via allowlisted Discord user ID**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-03T01:08:14Z
- **Completed:** 2026-02-03T01:11:32Z
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments

- User allowlist enforcement module with check_allowlisted_user function
- Discord bot with global @bot.check decorator preventing command bypass
- Test suite with 3 passing tests validating allowlist logic
- ping command for testing authorization flow

## Task Commits

Each task was committed atomically:

1. **Task 1: Create user allowlist enforcement** - `59296ac` (feat)
2. **Task 2: Create Discord bot with allowlist decorator** - `9c65989` (feat)
3. **Task 3: Test bot locally** - `2574ee7` (feat)

## Files Created/Modified

- `src/auth.py` - User allowlist enforcement via check_allowlisted_user function
- `src/bot.py` - Discord bot with global @bot.check decorator and ping command
- `tests/__init__.py` - Test suite marker
- `tests/test_auth.py` - Comprehensive auth tests with mocked Discord context
- `requirements.txt` - Added pytest>=8.0.0 and audioop-lts>=0.2.0

## Decisions Made

1. **Global @bot.check decorator** - Enforces allowlist at bot level rather than per-command decorators. Security-first approach: impossible to bypass, runs automatically for all commands, single point of enforcement.

2. **Deferred bot creation** - Created create_bot() function instead of instantiating bot at module import time. Avoids Python 3.14 asyncio event loop issue where bot initialization requires an event loop that doesn't exist yet at import time.

3. **audioop-lts dependency** - Python 3.13+ removed the audioop module that py-cord depends on. Added audioop-lts>=0.2.0 to provide compatibility layer.

4. **Independent auth testing** - Test allowlist logic via mocked Discord context rather than requiring live bot connection. Enables fast CI/CD testing without Discord API credentials.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added audioop-lts dependency for Python 3.14 compatibility**

- **Found during:** Task 1 (Auth module import)
- **Issue:** py-cord import failed with "ModuleNotFoundError: No module named 'audioop'" - audioop was removed in Python 3.13
- **Fix:** Added audioop-lts>=0.2.0 to requirements.txt and installed it
- **Files modified:** requirements.txt
- **Verification:** `from src.auth import check_allowlisted_user` succeeds
- **Commit:** 59296ac

**2. [Rule 3 - Blocking] Deferred bot creation to avoid asyncio event loop error**

- **Found during:** Task 2 (Bot module verification)
- **Issue:** `discord.Bot()` at module import time raised "RuntimeError: There is no current event loop in thread 'MainThread'" on Python 3.14
- **Fix:** Wrapped bot creation in create_bot() function called from main(), deferring instantiation until runtime when event loop exists
- **Files modified:** src/bot.py
- **Verification:** `from src.bot import create_bot` succeeds without runtime errors
- **Commit:** 9c65989

**3. [Rule 3 - Blocking] Added pytest to requirements**

- **Found during:** Task 3 (Running tests)
- **Issue:** pytest not installed - required for test execution
- **Fix:** Added pytest>=8.0.0 to requirements.txt and installed it
- **Files modified:** requirements.txt
- **Verification:** `python -m pytest tests/test_auth.py -v` runs successfully, 3 tests pass
- **Commit:** 2574ee7

---

**Total deviations:** 3 auto-fixed (3 blocking)
**Impact on plan:** All fixes necessary for Python 3.14 compatibility and test execution. No scope creep - just resolving technical blockers.

## Issues Encountered

None - plan executed smoothly with Python 3.14 compatibility fixes documented above.

## Next Phase Readiness

- ✅ Discord bot code complete with global allowlist enforcement
- ✅ Authorization cannot be bypassed (enforced at bot level)
- ✅ Error handler provides user-friendly rejection messages
- ✅ Tests verify allowlist logic (3/3 passing)
- ⚠️ Manual bot testing pending (requires Discord bot token and live connection)

**Ready for 01-03-PLAN.md** - Next step: Manual bot testing and Gmail integration

---
*Phase: 01-foundation-security*
*Completed: 2026-02-03*
