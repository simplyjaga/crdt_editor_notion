from dataclasses import dataclass


@dataclass(frozen=True)
class CRDTItem:
    item_id: str
    origin_id: str
    session_id: str
    logical_clock: int
    value: str
    deleted: bool = False
