-- 001-init-schema.sql
-- Crea el schema ORAFI + tablas base (accounts, audit_log, interest_history).
-- E2: los sinonimos publicos se crean en 002-synonyms.sql (separados).
-- E4: las tablas usan TRIGGER autonomousos en 004-autonomous-trigger.sql.

CREATE TABLE accounts (
    account_id      VARCHAR2(20) PRIMARY KEY,
    customer_name   VARCHAR2(255) NOT NULL,
    balance         NUMBER(15,2) NOT NULL CHECK (balance >= 0),
    status          VARCHAR2(20) DEFAULT 'OPEN' NOT NULL,
    opened_at       TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    closed_at       TIMESTAMP,
    CONSTRAINT accounts_status_chk CHECK (status IN ('OPEN','CLOSED','SUSPENDED'))
);

CREATE TABLE account_history (
    history_id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id      VARCHAR2(20) NOT NULL,
    action          VARCHAR2(50) NOT NULL,
    old_balance     NUMBER(15,2),
    new_balance     NUMBER(15,2),
    actor           VARCHAR2(100) DEFAULT USER NOT NULL,
    created_at      TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

CREATE TABLE audit_log (
    audit_id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name      VARCHAR2(100) NOT NULL,
    operation       VARCHAR2(10) NOT NULL,
    record_id       VARCHAR2(50),
    actor           VARCHAR2(100) DEFAULT USER NOT NULL,
    payload         CLOB,
    created_at      TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT audit_op_chk CHECK (operation IN ('INSERT','UPDATE','SELECT','DELETE'))
);

CREATE TABLE interest_history (
    history_id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id      VARCHAR2(20) NOT NULL,
    days            INTEGER NOT NULL,
    rate            NUMBER(5,4) NOT NULL,
    amount          NUMBER(15,2) NOT NULL,
    calculated_at   TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

CREATE TABLE monthly_close (
    close_id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    period          VARCHAR2(7) NOT NULL,
    closed_at       TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    closed_by       VARCHAR2(100) DEFAULT USER NOT NULL,
    CONSTRAINT monthly_close_period_uq UNIQUE (period),
    CONSTRAINT monthly_close_period_chk CHECK (REGEXP_LIKE(period, '^\d{4}-(0[1-9]|1[0-2])$'))
);

-- Grants para el schema ORAFI (usuario actual)
GRANT CONNECT, RESOURCE, DBA TO ORAFI;
GRANT UNLIMITED TABLESPACE TO ORAFI;