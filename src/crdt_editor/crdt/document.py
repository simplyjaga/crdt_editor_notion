from collections import defaultdict

from crdt_editor.models.crdt_item import CRDTItem


ROOT_ID = "ROOT"


class Document:
    def __init__(self) -> None:
        self._items: dict[str, CRDTItem] = {}

    def insert(self, item: CRDTItem) -> None:
        if item.item_id in self._items:
            raise ValueError(f"Duplicate item ID: {item.item_id}")

        if item.origin_id != ROOT_ID and item.origin_id not in self._items:
            raise ValueError(f"Unknown origin ID: {item.origin_id}")

        self._items[item.item_id] = item

    def to_text(self) -> str:
        children: dict[str, list[CRDTItem]] = defaultdict(list)

        for item in self._items.values():
            children[item.origin_id].append(item)

        for siblings in children.values():
            siblings.sort(
                key=lambda item: (
                    item.logical_clock,
                    item.session_id,
                    item.item_id,
                )
            )

        result: list[str] = []

        def visit(parent_id: str) -> None:
            for item in children[parent_id]:
                if not item.deleted:
                    result.append(item.value)

                # Visit descendants even when this item is deleted.
                visit(item.item_id)

        visit(ROOT_ID)
        return "".join(result)
