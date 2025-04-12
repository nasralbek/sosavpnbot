create_users_table = """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        balance INTEGER DEFAULT 0,
                        invited_by INTEGER,
                        referrals INTEGER DEFAULT 0
                    )
                """
select_user_from_users = "SELECT * FROM users WHERE user_id = ?"
#insert_user_to_users = "UPDATE users SET balance = balance + 50, referrals = referrals + 1 WHERE user_id = ?"
insert_user_to_users_only_user_id_and_balance ="INSERT INTO users (user_id, balance) VALUES (?, ?)"
select_balance_from_users =  "SELECT balance FROM users WHERE user_id = ?"
select_referals_from_users = "SELECT referrals FROM users WHERE user_id = ?"
update_user_balance = "UPDATE users SET balance = ? WHERE user_id = ?"
update_user_referals = "UPDATE users SET referrals = ? WHERE user_id = ?"
select_refs_from_users = "SELECT balance FROM users WHERE user_id = ?"
insert_new_user = "INSERT INTO users (user_id, balance, invited_by,referrals) VALUES (?, ?, ?, ?)"