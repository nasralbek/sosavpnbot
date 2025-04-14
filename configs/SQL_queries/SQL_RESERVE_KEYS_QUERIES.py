
create_reserve_keys_table = """
CREATE TABLE IF NOT EXISTS reserve_keys (
    row INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL,
    issued BOOL NOT NULL DEFAULT FALSE
)"""

get_key = """
SELECT key from reserve_keys where issued = FALSE
"""
issue_key = """
UPDATE reserve_keys
set issued = TRUE
where key = ?
"""


add_key ="""
INSERT INTO reserve_keys (key) VALUES (?)
"""