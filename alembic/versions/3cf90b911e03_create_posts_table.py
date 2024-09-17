"""create posts table

Revision ID: 3cf90b911e03
Revises: 
Create Date: 2024-09-17 19:44:47.203424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cf90b911e03'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False, primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
    pass
