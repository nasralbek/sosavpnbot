create_keys_table = """
                    CREATE TABLE IF NOT EXISTS keys (
                        row INTEGER PRIMARY KEY AUTOINCREMENT,
                        key TEXT,
                        issued BOOL NOT NULL,
                        user_id INTEGER NOT NULL,
                        uuid TEXT NOT NULL
                    )
                """

add_key = """
    INSERT INTO keys (key,user_id, issued) 
    VALUES (?, ?, ?)
"""
add_pending = """
INSERT INTO keys (user_id, issued,uuid) 
VALUES (?, ?, ?)
"""

select_by_issued  = """
SELECT user_id,uuid FROM keys WHERE issued = ?
"""

issue_key = """UPDATE keys SET key = ?, issued = ?
WHERE uuid = ?"""



