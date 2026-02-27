# PR-3 Self-Review: Add regression test — non-owner editor cannot edit exploration

## What changed and why?
Added `test_non_owner_editor_cannot_edit_exploration` to `EditExplorationTests`
in `core/controllers/acl_decorators_test.py`. The existing tests covered owner
allowed, guest denied, and banned user denied — but not the case where another
authenticated user attempts to edit an exploration they do not own. This is the
lateral privilege escalation gap.

## Why is this the right test layer?
Integration level is correct here. The goal is to validate that the
`can_edit_exploration` decorator correctly rejects an authenticated but
unauthorized user through the full decorator chain — no mocks, no shortcuts.

## What could still break / what is not covered?
- The `can_save_exploration` decorator has the same gap and is not covered by
  this PR
- Only the private exploration case is tested; the published exploration case
  for a non-owner is not explicitly tested here (though moderators can edit
  published explorations, a plain other_editor cannot)

## What risks or follow-ups remain?
- A follow-up PR could add the same test to `SaveExplorationTests` for
  completeness
- The issue acceptance criteria listed 403 as the expected status code, but the
  codebase actually returns 401 for `UnauthorizedUserException` — this is
  correct behavior and the test reflects reality, but the issue description
  should be noted as inaccurate on that point