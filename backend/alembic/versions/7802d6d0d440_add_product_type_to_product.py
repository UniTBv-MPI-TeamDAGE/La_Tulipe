"""add product_type to product

Revision ID: 7802d6d0d440
Revises: 173d4913137e
Create Date: 2026-04-01 15:22:08.568714

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7802d6d0d440'
down_revision: Union[str, Sequence[str], None] = '173d4913137e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    product_type_enum = sa.Enum(
        'INDIVIDUAL',
        'BOUQUET',
        name='product_type_enum',
    )

    product_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'products',
        sa.Column(
            'product_type',
            product_type_enum,
            nullable=False,
            server_default='INDIVIDUAL',
        ),
    )
    op.alter_column('products', 'product_type', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    product_type_enum = sa.Enum(
        'INDIVIDUAL',
        'BOUQUET',
        name='product_type_enum',
    )

    op.drop_column('products', 'product_type')
    product_type_enum.drop(op.get_bind(), checkfirst=True)
