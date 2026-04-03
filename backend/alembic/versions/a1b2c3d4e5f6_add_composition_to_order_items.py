"""add composition field to order_items

Revision ID: a1b2c3d4e5f6
Revises: 9f31b6b0c4a2
Create Date: 2026-04-03 10:15:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "9f31b6b0c4a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("order_items", sa.Column("composition", sa.JSON(), nullable=True))
    op.alter_column(
        "order_items",
        "product_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "order_items",
        "product_name",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "order_items",
        "product_name",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "order_items",
        "product_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_column("order_items", "composition")
