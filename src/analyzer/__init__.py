"""analyzer: utilities for sorting and analysing weighted items.

The core logic lives in :mod:`analyzer.analyser`; the names are
re-exported here so `from analyzer import sort_by_weight` keeps
working.
"""

from .analyser import get_heaviest, sort_by_weight

__all__ = ["sort_by_weight", "get_heaviest"]


def main() -> None:
    """Demo entry point: sort a small sample dataset and print the result."""
    data = [
        {"name": "apple", "weight": "150"},
        {"name": "grape", "weight": "5"},
        {"name": "melon", "weight": "1200.5"},
        {"name": "pumpkin", "weight": 1200.5},
    ]
    print(sort_by_weight(data))
    print(get_heaviest(data))


if __name__ == "__main__":
    main()
    print("\n\nDemo finished.")
