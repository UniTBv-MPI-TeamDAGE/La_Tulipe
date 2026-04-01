"""seed default colors

Revision ID: d1e2f3a4b5c6
Revises: 7bd594eaf60d
Create Date: 2026-04-01 16:55:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "d1e2f3a4b5c6"
down_revision: Union[str, Sequence[str], None] = "7bd594eaf60d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DEFAULT_COLORS: list[dict[str, str]] = [
    {"name": "Red", "hex_code": "#FF0000"},
    {"name": "White", "hex_code": "#FFFFFF"},
    {"name": "Pink", "hex_code": "#FFC0CB"},
    {"name": "Yellow", "hex_code": "#FFD700"},
    {"name": "Orange", "hex_code": "#FFA500"},
    {"name": "Purple", "hex_code": "#800080"},
    {"name": "Blue", "hex_code": "#0000FF"},
    {"name": "Cream", "hex_code": "#FFFDD0"},
]


def upgrade() -> None:
    """Upgrade schema."""
    colors_table = sa.table(
        "colors",
        sa.column("name", sa.String()),
        sa.column("hex_code", sa.String()),
    )

    op.bulk_insert(colors_table, DEFAULT_COLORS)


def downgrade() -> None:
    """Downgrade schema."""
    color_names = tuple(color["name"] for color in DEFAULT_COLORS)
    op.execute(
        sa.text("DELETE FROM colors WHERE name IN :names").bindparams(
            sa.bindparam("names", value=color_names, expanding=True)
        )
    )
