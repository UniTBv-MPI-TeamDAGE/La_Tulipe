"""add product details and product colors

Revision ID: f4a7c2d9e1b3
Revises: d1e2f3a4b5c6
Create Date: 2026-04-01 18:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "f4a7c2d9e1b3"
down_revision: Union[str, Sequence[str], None] = "d1e2f3a4b5c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    product_season_enum = sa.Enum(
        "ALL_SEASON",
        "SPRING",
        "SUMMER",
        "AUTUMN",
        "WINTER",
        name="product_season_enum",
    )
    product_season_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "products",
        sa.Column("description", sa.String(), nullable=False, server_default=""),
    )
    op.add_column(
        "products",
        sa.Column(
            "season",
            product_season_enum,
            nullable=False,
            server_default="ALL_SEASON",
        ),
    )
    op.alter_column("products", "description", server_default=None)
    op.alter_column("products", "season", server_default=None)

    op.create_table(
        "product_colors",
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("color_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["color_id"], ["colors.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("product_id", "color_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    product_season_enum = sa.Enum(
        "ALL_SEASON",
        "SPRING",
        "SUMMER",
        "AUTUMN",
        "WINTER",
        name="product_season_enum",
    )

    op.drop_table("product_colors")
    op.drop_column("products", "season")
    op.drop_column("products", "description")
    product_season_enum.drop(op.get_bind(), checkfirst=True)
