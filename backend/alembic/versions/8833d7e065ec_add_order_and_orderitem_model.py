"""add order and orderitem model

Revision ID: 8833d7e065ec
Revises: f4a7c2d9e1b3
Create Date: 2026-04-01 17:20:28.868030

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "8833d7e065ec"
down_revision: Union[str, Sequence[str], None] = "f4a7c2d9e1b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
