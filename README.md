# sample_analyser

This is a sample project.

## Quick start

From the project root:

```bash
uv sync                      # one-time: create .venv and install everything
uv run sample-analyser-web   # start the web app + API
```

Then open **http://127.0.0.1:5000** in your browser. Stop the server with
`Ctrl+C`.

To try the API without the browser, in another terminal:

```bash
curl -s -X POST http://127.0.0.1:5000/api/heaviest \
  -H 'Content-Type: application/json' \
  -d '{"items": [{"name": "apple", "weight": "150"}, {"name": "grape", "weight": "5"}]}'
# {"heaviest":[{"name":"apple","weight":"150"}]}
```

## Description

Utilities for sorting and analysing weighted items. Weights may be numbers
(`1200.5`) or numeric strings (`"1200.5"`); they are compared as floats.

- `sort_by_weight(items, reverse=False)` — return a **new** list of
  `{'name': ..., 'weight': ...}` dicts sorted by weight.
  - Raises `TypeError` if `items` is not a list.
  - Raises `ValueError` if an item is missing `weight` or has a
    non-numeric weight.
- `get_heaviest(items)` — return all items that share the **highest**
  weight, ties included. Returns `[]` for an empty list.

## Installation

Requires [uv](https://docs.astral.sh/uv/). From the project root:

```bash
uv sync
```

This creates a virtual environment at `.venv/`, installs the package
(editably) and the dev dependencies, and locks them in `uv.lock`.

## Usage

### Command line

```bash
uv run sample-analyser
```

Prints a small demo dataset sorted by weight, plus the heaviest item(s).

### As a library

```python
from sample_analyser import sort_by_weight, get_heaviest

data = [
    {"name": "apple", "weight": "150"},
    {"name": "grape", "weight": "5"},
]

sort_by_weight(data)
# [{'name': 'grape', 'weight': '5'}, {'name': 'apple', 'weight': '150'}]

get_heaviest(data)
# [{'name': 'apple', 'weight': '150'}]
```

### Web app & JSON API

```bash
uv run sample-analyser-web
```

Serves a web frontend at http://127.0.0.1:5000 (paste a JSON array of items,
sort them ascending/descending, or highlight the heaviest) and a JSON API.

#### API

All endpoints accept and return JSON. Errors come back as
`{"error": "<message>"}` with status `400` (bad request), `404` or `405`.

| Endpoint | Method | Body | Response |
|---|---|---|---|
| `/api/sort` | `POST` | `{"items": [...], "reverse": false}` | `{"sorted": [...]}` |
| `/api/heaviest` | `POST` | `{"items": [...]}` | `{"heaviest": [...]}` |
| `/api/health` | `GET` | — | `{"status": "ok"}` |

Example:

```bash
curl -s -X POST http://127.0.0.1:5000/api/heaviest \
  -H 'Content-Type: application/json' \
  -d '{"items": [{"name": "apple", "weight": "150"}, {"name": "grape", "weight": "5"}]}'
# {"heaviest":[{"name":"apple","weight":"150"}]}
```

`items` must be a list of `{...}` objects, each with a (numeric or numeric
string) `weight`. A missing or non-numeric weight returns `400`.

## Development

Setting up on **Windows**? Follow the step-by-step guide:
[`docs/development-windows.md`](docs/development-windows.md) — toolchain
(Git, Python, pip, uv), running the web app, and testing the API with HTTPie.

```bash
uv add <package>          # add a runtime dependency
uv add --dev <package>    # add a dev dependency
uv run pytest             # run tests (dev group)
uv build                  # build a wheel/sdist into dist/
uv publish                # publish to PyPI
```
