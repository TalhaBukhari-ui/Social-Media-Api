"""add foreign key column to posts

Revision ID: b545712b1e6f
Revises: 43e2660c5e37
Create Date: 2024-09-17 21:02:30.190681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b545712b1e6f'
down_revision: Union[str, None] = '43e2660c5e37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',
    local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
