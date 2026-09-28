import sqlite3

from crdt_editor.models.crdt_item import CRDTItem


def insert_item(connection: sqlite3.Connection, item: CRDTItem) -> None:
    connection.execute(
        """
        INSERT INTO crdt_items (
            item_id, origin_id, session_id,
            logical_clock, value, deleted
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            item.item_id,
            item.origin_id,
            item.session_id,
            item.logical_clock,
            item.value,
            int(item.deleted),
        ),
    )
    connection.commit()


def get_item(
    connection: sqlite3.Connection,
    item_id: str,
) -> CRDTItem | None:
    row = connection.execute(
        """
        SELECT item_id, origin_id, session_id,
               logical_clock, value, deleted
        FROM crdt_items
        WHERE item_id = ?
        """,
        (item_id,),
    ).fetchone()

    if row is None:
        return None

    return CRDTItem(
        item_id=row[0],
        origin_id=row[1],
        session_id=row[2],
        logical_clock=row[3],
        value=row[4],
        deleted=bool(row[5]),
    )
