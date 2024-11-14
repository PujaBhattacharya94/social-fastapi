"""add published column to posts table

Revision ID: deca3221cfe5
Revises: 973fcf2f8d81
Create Date: 2024-11-14 10:45:37.926601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'deca3221cfe5'
down_revision: Union[str, None] = '973fcf2f8d81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),nullable=False,
                                      server_default=sa.text('True')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    pass
