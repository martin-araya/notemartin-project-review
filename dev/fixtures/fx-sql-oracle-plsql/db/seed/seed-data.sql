-- seed-data.sql
INSERT INTO accounts (account_id, customer_name, balance, status)
VALUES
    ('acct-001', 'Alice Corp', 10000.00, 'OPEN'),
    ('acct-002', 'Bob SA', 5000.00, 'OPEN'),
    ('acct-003', 'Charlie LLC', 0.00, 'CLOSED');

INSERT INTO account_history (account_id, action, old_balance, new_balance, actor)
VALUES
    ('acct-001', 'INSERT', NULL, 10000.00, 'admin'),
    ('acct-002', 'INSERT', NULL, 5000.00, 'admin'),
    ('acct-003', 'UPDATE', 1000.00, 0.00, 'admin');

INSERT INTO interest_history (account_id, days, rate, amount)
VALUES
    ('acct-001', 30, 0.0025, 20.55),
    ('acct-002', 30, 0.0025, 10.27);

INSERT INTO monthly_close (period)
VALUES
    ('2025-01');