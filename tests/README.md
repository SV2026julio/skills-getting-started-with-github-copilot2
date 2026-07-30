# Backend Test Suite

This directory contains backend API tests for the FastAPI app.

## Structure

- `conftest.py`: shared pytest fixtures.
- `test_app.py`: endpoint behavior tests (success and error paths).

## Test Strategy

The app stores activity data in memory. To avoid flaky tests caused by shared state:

- `reset_activities_state` restores `activities` before each test.
- Each test can safely mutate data without affecting other tests.

## Run Tests

From the repository root:

```bash
pytest -q
```

Run only backend API tests:

```bash
pytest -q tests/test_app.py
```

Run a single test by name:

```bash
pytest -q tests/test_app.py -k signup
```

## Coverage Guidelines

When adding new endpoints, include tests for:

- success path (`2xx`)
- invalid input (`4xx`)
- missing resources (`404`)
- state mutation verification (read back data after write)

## Adding New Tests

1. Add tests to `test_app.py` or create a new `test_*.py` file.
2. Reuse the `client` fixture from `conftest.py`.
3. Keep assertions explicit for status code and response payload.
4. Run `pytest -q` before committing.
