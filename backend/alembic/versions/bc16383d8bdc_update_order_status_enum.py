"""update order_status enum

Revision ID: bc16383d8bdc
Revises: 6a1aa15e390c
Create Date: 2026-04-01 17:57:26.937003

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bc16383d8bdc'
down_revision: Union[str, Sequence[str], None] = '6a1aa15e390c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE order_status_enum RENAME TO order_status_enum_old")

    new_order_status_enum = sa.Enum(
        "PENDING",
        "CONFIRMED",
        "DELIVERED",
        "CANCELLED",
        name="order_status_enum",
    )
    new_order_status_enum.create(op.get_bind(), checkfirst=False)

    op.execute(
        """
        ALTER TABLE orders
        ALTER COLUMN status TYPE order_status_enum
        USING (
            CASE
                WHEN status::text = 'PLACED' THEN 'PENDING'
                ELSE status::text
            END
        )::order_status_enum
        """
    )

    op.execute("DROP TYPE order_status_enum_old")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE order_status_enum RENAME TO order_status_enum_new")

    old_order_status_enum = sa.Enum(
        "PLACED",
        "DELIVERED",
        "CANCELLED",
        name="order_status_enum",
    )
    old_order_status_enum.create(op.get_bind(), checkfirst=False)

    op.execute(
        """
        ALTER TABLE orders
        ALTER COLUMN status TYPE order_status_enum
        USING (
            CASE
                WHEN status::text IN ('PENDING', 'CONFIRMED') THEN 'PLACED'
                ELSE status::text
            END
        )::order_status_enum
        """
    )

    op.execute("DROP TYPE order_status_enum_new")
