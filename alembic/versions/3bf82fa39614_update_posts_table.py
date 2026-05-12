"""update posts table

Revision ID: 3bf82fa39614
Revises: 
Create Date: 2026-05-12 13:31:01.486966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bf82fa39614'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("last_updated_at", sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "last_updated_at")
    pass
