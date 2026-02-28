# Self-Review: PR #11 — Add backend shard registration check to CI validation

## What changed and why?

Extended `scripts/check_tests_are_captured_in_ci.py` with a new function
`get_unregistered_backend_test_modules()` that scans all `*_test.py` files
on disk across `core/`, `scripts/`, `extensions/`, and the repo root, then
diffs them against every module registered in `scripts/backend_test_shards.json`.

Before this change, a developer could create a backend test file and forget
to register it in the shards file. CI would run silently and those tests
would never execute — invisible coverage loss with no warning anywhere.
This check catches that gap at CI time and emits an actionable error message
naming each missing module and linking to the wiki.

Also registered two real modules discovered by the new check that were
previously missing from the shards file:

- `core.tests.build_sources.extensions.base_test`
- `core.tests.build_sources.extensions.models_test`

## Why is this the right test layer?

This is infrastructure/script testing, not production code testing.
The right layer is a unit test of the checker script itself, run inside
the backend test suite. The three new tests in
`check_tests_are_captured_in_ci_test.py` test exactly the three behaviors
that matter: passing case, failing case, and root-level file handling.

## What could still break / what is not covered?

- If a new top-level directory is added for test files and is not in
  `dirs_to_scan`, files there will not be caught. That requires a manual
  update to the constant in the function.
- The inverse check (shard entries pointing to files that no longer exist
  on disk) is not implemented. A ghost entry would cause `run_backend_tests.py`
  to fail with a cryptic import error rather than a clean message.

## What risks or follow-ups remain?

- Follow-up: add ghost-entry detection (shard entries with no corresponding
  file on disk).
- The 14 pre-existing test errors in `CheckTestsAreCapturedInCiTest` are a
  local environment issue (duplicate superadmin user in test datastore) and
  are not caused by this PR. All 3 new tests pass cleanly.
