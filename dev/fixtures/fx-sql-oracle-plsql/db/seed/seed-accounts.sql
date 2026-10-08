-- seed-accounts.sql (cuentas adicionales para tests)
INSERT INTO accounts (account_id, customer_name, balance, status)
VALUES
    ('acct-test-1', 'Test Customer 1', 1500.00, 'OPEN'),
    ('acct-test-2', 'Test Customer 2', 0.00, 'OPEN');

-- (fixture + accounts adicionales ya cubiertos arriba)

SELECT 'seed-accounts: cuentas test cargadas' AS marker FROM DUAL;