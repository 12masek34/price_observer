"""product

Revision ID: f2292313fca9
Revises: 5aa05c98171f
Create Date: 2025-01-27 17:26:52.125628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2292313fca9'
down_revision: Union[str, None] = '5aa05c98171f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.add_column('subscriptions', sa.Column('user_id', sa.Integer(), nullable=False))
    op.add_column('subscriptions', sa.Column('chat_id', sa.Integer(), nullable=False))
    op.add_column('subscriptions', sa.Column('proudct_id', sa.Integer(), nullable=True))
    op.add_column('subscriptions', sa.Column('user_name', sa.String(), nullable=True))
    op.add_column('subscriptions', sa.Column('url', sa.String(), nullable=False))
    op.create_index(op.f('ix_subscriptions_chat_id'), 'subscriptions', ['chat_id'], unique=False)
    op.create_index(op.f('ix_subscriptions_user_id'), 'subscriptions', ['user_id'], unique=False)
    op.create_foreign_key(None, 'subscriptions', 'products', ['proudct_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subscriptions', type_='foreignkey')
    op.drop_index(op.f('ix_subscriptions_user_id'), table_name='subscriptions')
    op.drop_index(op.f('ix_subscriptions_chat_id'), table_name='subscriptions')
    op.drop_column('subscriptions', 'url')
    op.drop_column('subscriptions', 'user_name')
    op.drop_column('subscriptions', 'proudct_id')
    op.drop_column('subscriptions', 'chat_id')
    op.drop_column('subscriptions', 'user_id')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###
