from typing import Any


def sort_by_weight(items: list[dict[str, Any]], reverse: bool = False) -> list[dict[str, Any]]:
    """Return a new list of {'name': ..., 'weight': ...} dicts sorted by weight.

    Weights may be numbers or numeric strings (e.g. '12.5').
    Raises ValueError if an item is missing 'weight' or has a non-numeric weight.
    """
    if not isinstance(items, list):
        raise TypeError(f"Expected a list of dicts, got {type(items).__name__}")

    def weight_key(item: dict[str, Any]) -> float:
        if not isinstance(item, dict) or "weight" not in item:
            raise ValueError(f"Item is missing 'weight': {item!r}")
        try:
            return float(item["weight"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid weight for item {item!r}") from exc

    return sorted(items, key=weight_key, reverse=reverse)


def get_heaviest(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return all items that share the highest weight (ties included).

    Returns an empty list if items is empty.
    """
    sorted_items = sort_by_weight(items, reverse=True)
    if not sorted_items:
        return []

    max_weight = float(sorted_items[0]["weight"])
    heaviest = []
    for item in sorted_items:
        if float(item["weight"]) != max_weight:
            break
        heaviest.append(item)
    return heaviest


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
