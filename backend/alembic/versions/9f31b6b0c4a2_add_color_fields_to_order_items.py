"""add color fields to order_items

Revision ID: 9f31b6b0c4a2
Revises: 65c6188c1698
Create Date: 2026-04-03 09:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f31b6b0c4a2"
down_revision: Union[str, Sequence[str], None] = "65c6188c1698"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("order_items", sa.Column("color_id", sa.Integer(), nullable=True))
    op.add_column("order_items", sa.Column("color_name", sa.String(), nullable=True))
    op.create_foreign_key(
        "fk_order_items_color_id_colors",
        "order_items",
        "colors",
        ["color_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_order_items_color_id_colors", "order_items", type_="foreignkey")
    op.drop_column("order_items", "color_name")
    op.drop_column("order_items", "color_id")
