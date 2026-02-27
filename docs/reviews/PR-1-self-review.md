# Self-Review: PR-1 — Unpublish removes exploration from summaries endpoint

## What changed and why?
Added `test_unpublish_removes_exploration_from_summaries` to
`ExplorationSummariesHandlerTests` in `core/controllers/library_test.py`.

The test publishes an exploration (done in setUp), confirms it appears in
`EXPLORATION_SUMMARIES_DATA_URL`, calls `rights_manager.unpublish_exploration`
as a moderator, then asserts the exploration is gone from the same endpoint.
This closes the regression gap in Issue #1 — previously there was zero test
coverage for the unpublish path in the library controller.

## Why is this the right test layer?
Integration — the test exercises the real `rights_manager.unpublish_exploration`
domain call, the real datastore emulator, and the real library HTTP handler
end-to-end. No mocks are needed. A unit test would not catch a bug where the
summary index fails to update after a rights change, which is exactly the
regression risk this test protects against.

## What could still break / what's not covered?
- Only checks the public summaries endpoint (include_private_explorations=False)
- Does not test re-publishing after unpublishing (round-trip)
- Does not test the case where a moderator unpublishes someone else's exploration
  vs. the owner unpublishing their own

## What risks or follow-ups remain?
- The Error -11 datastore emulator crash on first attempt is a known Mac/Java
  infrastructure issue unrelated to the test logic. The test passes on retry.
- Follow-up: add a test verifying re-publishing after unpublish restores the
  exploration to summaries.
