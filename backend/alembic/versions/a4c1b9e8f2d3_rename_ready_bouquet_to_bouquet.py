"""rename READY_BOUQUET enum value to BOUQUET

Revision ID: a4c1b9e8f2d3
Revises: 7802d6d0d440
Create Date: 2026-04-01 16:05:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "a4c1b9e8f2d3"
down_revision: Union[str, Sequence[str], None] = "7802d6d0d440"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'product_type_enum' AND e.enumlabel = 'READY_BOUQUET'
            ) AND NOT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'product_type_enum' AND e.enumlabel = 'BOUQUET'
            ) THEN
                ALTER TYPE product_type_enum RENAME VALUE 'READY_BOUQUET' TO 'BOUQUET';
            END IF;
        END $$;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'product_type_enum' AND e.enumlabel = 'BOUQUET'
            ) AND NOT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_enum e ON e.enumtypid = t.oid
                WHERE t.typname = 'product_type_enum' AND e.enumlabel = 'READY_BOUQUET'
            ) THEN
                ALTER TYPE product_type_enum RENAME VALUE 'BOUQUET' TO 'READY_BOUQUET';
            END IF;
        END $$;
        """
    )
