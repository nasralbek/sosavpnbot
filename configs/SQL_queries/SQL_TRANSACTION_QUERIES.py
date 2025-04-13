create_transactions_table = """
                    CREATE TABLE IF NOT EXISTS transactions (
                        row INTEGER PRIMARY KEY AUTOINCREMENT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        user_id INTEGER NOT NULL,
                        amount INTEGER NOT NULL,
                        status TEXT NOT NULL,
                        key_requested BOOL DEFAULT FALSE, 
                        uuid TEXT NOT NULL,
                        payment_id TEXT NOT NULL
                    )
                """
insert_transaction = """
    INSERT INTO transactions (user_id, amount, status,uuid,payment_id) 
    VALUES (?, ?, ?, ?, ?)
"""
set_status = """UPDATE transactions SET status = ? WHERE uuid = ?"""
get_status = """SELECT status FROM transactions WHERE uuid = ?"""
get_user_id = """SELECT user_id FROM transactions WHERE uuid = ?"""
get_waiting_transactions = """SELECT uuid FROM transactions WHERE status = 'waiting'"""
set_key_requested= """UPDATE transactions SET key_requested = ? WHERE uuid = ?"""
get_payment_id = """SELECT payment_id FROM transactions WHERE uuid = ?"""