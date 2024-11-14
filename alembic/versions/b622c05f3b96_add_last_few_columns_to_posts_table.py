"""add last few columns to posts table

Revision ID: b622c05f3b96
Revises: 994cb193f208
Create Date: 2024-11-14 19:38:03.062368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b622c05f3b96'
down_revision: Union[str, None] = '994cb193f208'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','created_at')
    pass
