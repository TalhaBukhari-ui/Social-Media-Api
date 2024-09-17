"""add last few cols to posts table

Revision ID: f7bf572728f5
Revises: b545712b1e6f
Create Date: 2024-09-17 21:09:00.358233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7bf572728f5'
down_revision: Union[str, None] = 'b545712b1e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default= sa.text('NOW()')),)

def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
