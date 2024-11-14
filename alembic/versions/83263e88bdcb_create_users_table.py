"""create users table

Revision ID: 83263e88bdcb
Revises: deca3221cfe5
Create Date: 2024-11-14 11:04:02.649562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83263e88bdcb'
down_revision: Union[str, None] = 'deca3221cfe5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #creating users table
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    
    
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
