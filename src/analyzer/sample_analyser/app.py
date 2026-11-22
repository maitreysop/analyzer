"""Flask web app and JSON API around the sample_analyser utilities.

Run with:
    uv run sample-analyser-web
"""

from __future__ import annotations

from typing import Any

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from . import get_heaviest, sort_by_weight

app = Flask(__name__)


def _parse_items_payload() -> tuple[Any, bool, str | None]:
    """Extract ``items`` and the optional ``reverse`` flag from the request.

    Returns ``(items, reverse, error)``; on error, ``error`` holds a
    human-readable message and the other values are meaningless.
    """
    if not request.is_json:
        return None, False, "Content-Type must be application/json"

    payload = request.get_json(silent=True)
    if payload is None:
        return None, False, "Request body must be valid JSON"
    if not isinstance(payload, dict):
        return None, False, "Request body must be a JSON object"

    unknown = set(payload) - {"items", "reverse"}
    if unknown:
        return None, False, f"Unknown field(s): {', '.join(sorted(unknown))}"
    if "items" not in payload:
        return None, False, "Missing required field: 'items'"

    reverse = payload.get("reverse", False)
    if not isinstance(reverse, bool):
        return None, False, "'reverse' must be a boolean"

    return payload["items"], reverse, None


def _apply(fn: Any, items: Any, response_key: str, reverse: bool | None = None) -> tuple[int, Any]:
    """Apply an analyser function and map its errors onto HTTP responses.

    ``reverse`` is passed to ``fn`` when not ``None`` (only ``sort_by_weight``
    takes it).
    """
    try:
        if reverse is None:
            result = fn(items)
        else:
            result = fn(items, reverse=reverse)
        return 200, {response_key: result}
    except TypeError as exc:
        return 400, {"error": str(exc)}
    except ValueError as exc:
        return 400, {"error": str(exc)}


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.get("/api/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@app.post("/api/sort")
def api_sort() -> tuple[Any, int]:
    items, reverse, error = _parse_items_payload()
    if error:
        return jsonify(error=error), 400

    status, body = _apply(sort_by_weight, items, "sorted", reverse=reverse)
    return jsonify(body), status


@app.post("/api/heaviest")
def api_heaviest() -> tuple[Any, int]:
    items, _, error = _parse_items_payload()
    if error:
        return jsonify(error=error), 400

    status, body = _apply(get_heaviest, items, "heaviest")
    return jsonify(body), status


@app.errorhandler(HTTPException)
def json_error(exc: HTTPException) -> tuple[Any, int]:
    """Return errors (404, 405, ...) as JSON, not HTML."""
    return jsonify(error=exc.description), exc.code


def main() -> None:
    """Start the development web server."""
    app.run(host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
