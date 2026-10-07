"""seed data (trampa E06: data migration)

Revision ID: 002_seed_data
Revises: 001_initial
Create Date: 2026-10-07

Trampa E06: esta migration no es solo schema. Ademas de cambiar la
tabla, ejecuta INSERTs para backfill de datos iniciales.
"""
from alembic import op
import sqlalchemy as sa


revision = "002_seed_data"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # E06: op.execute con INSERTs no es solo schema migration.
    op.execute(
        "INSERT INTO users (id, email, hashed_password, is_active, created_at) "
        "VALUES (1, 'seed@fxfast.local', 'hashed_seed', 1, '2026-10-07 00:00:00')"
    )
    op.execute(
        "INSERT INTO webhooks (id, url, event_type, secret, is_active, created_at) "
        "VALUES (1, 'https://example.test/hook', 'user.created', 'secret-seed', 1, '2026-10-07 00:00:00')"
    )


def downgrade() -> None:
    op.execute("DELETE FROM webhooks WHERE id = 1")
    op.execute("DELETE FROM users WHERE id = 1")