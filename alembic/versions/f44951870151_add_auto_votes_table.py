"""add auto votes table

Revision ID: f44951870151
Revises: f7bf572728f5
Create Date: 2024-09-17 21:22:22.426515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f44951870151'
down_revision: Union[str, None] = 'f7bf572728f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.alter_column('posts', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'created_at',
               existing_type=sa.TIMESTAMP(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_table('votes')
    # ### end Alembic commands ###
