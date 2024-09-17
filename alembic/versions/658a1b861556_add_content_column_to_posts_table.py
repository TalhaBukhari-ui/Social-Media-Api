"""add content column to posts table

Revision ID: 658a1b861556
Revises: 3cf90b911e03
Create Date: 2024-09-17 20:31:04.047556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '658a1b861556'
down_revision: Union[str, None] = '3cf90b911e03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
