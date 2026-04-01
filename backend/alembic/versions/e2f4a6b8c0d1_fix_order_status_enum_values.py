"""fix order status enum values

Revision ID: e2f4a6b8c0d1
Revises: bc16383d8bdc
Create Date: 2026-04-01 20:40:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "e2f4a6b8c0d1"
down_revision: Union[str, Sequence[str], None] = "bc16383d8bdc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        DO $$
        DECLARE
            has_placed boolean;
            has_pending boolean;
            has_confirmed boolean;
        BEGIN
            SELECT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'order_status_enum' AND e.enumlabel = 'PLACED'
            ) INTO has_placed;

            SELECT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'order_status_enum' AND e.enumlabel = 'PENDING'
            ) INTO has_pending;

            SELECT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'order_status_enum' AND e.enumlabel = 'CONFIRMED'
            ) INTO has_confirmed;

            IF has_placed THEN
                ALTER TYPE order_status_enum RENAME TO order_status_enum_old;

                CREATE TYPE order_status_enum AS ENUM (
                    'PENDING',
                    'CONFIRMED',
                    'DELIVERED',
                    'CANCELLED'
                );

                ALTER TABLE orders
                ALTER COLUMN status TYPE order_status_enum
                USING (
                    CASE
                        WHEN status::text = 'PLACED' THEN 'PENDING'
                        ELSE status::text
                    END
                )::order_status_enum;

                DROP TYPE order_status_enum_old;
            ELSIF has_pending AND NOT has_confirmed THEN
                ALTER TYPE order_status_enum ADD VALUE 'CONFIRMED';
            END IF;
        END $$;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DO $$
        DECLARE
            has_pending boolean;
            has_confirmed boolean;
            has_placed boolean;
        BEGIN
            SELECT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'order_status_enum' AND e.enumlabel = 'PENDING'
            ) INTO has_pending;

            SELECT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'order_status_enum' AND e.enumlabel = 'CONFIRMED'
            ) INTO has_confirmed;

            SELECT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'order_status_enum' AND e.enumlabel = 'PLACED'
            ) INTO has_placed;

            IF (has_pending OR has_confirmed) AND NOT has_placed THEN
                ALTER TYPE order_status_enum RENAME TO order_status_enum_new;

                CREATE TYPE order_status_enum AS ENUM (
                    'PLACED',
                    'DELIVERED',
                    'CANCELLED'
                );

                ALTER TABLE orders
                ALTER COLUMN status TYPE order_status_enum
                USING (
                    CASE
                        WHEN status::text IN ('PENDING', 'CONFIRMED') THEN 'PLACED'
                        ELSE status::text
                    END
                )::order_status_enum;

                DROP TYPE order_status_enum_new;
            END IF;
        END $$;
        """
    )
