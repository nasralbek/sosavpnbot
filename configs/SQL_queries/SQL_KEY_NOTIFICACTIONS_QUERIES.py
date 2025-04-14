create_keys_notifications_table = """
CREATE TABLE IF NOT EXISTS keys_notifications (
    row INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid_in_keys TEXT NOT NULL,
    notified BOOL NOT NULL
)
"""

add_notification = """
INSERT INTO keys_notifications (uuid_in_keys,notified)
VALUES (?, ?)
"""

set_notified = """
UPDATE keys_notifications 
SET notified = ?
WHERE uuid_in_keys = ?
"""

get_by_notified = """
SELECT uuid_in_keys
FROM keys_notifications
WHERE notified = ?"""
