import sqlite3


def create_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS crdt_items (
            item_id TEXT PRIMARY KEY,
            origin_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            logical_clock INTEGER NOT NULL,
            value TEXT NOT NULL,
            deleted INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    connection.commit()
