"""fix name

Revision ID: c82a6137803b
Revises: f2292313fca9
Create Date: 2025-01-28 11:26:16.403445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c82a6137803b'
down_revision: Union[str, None] = 'f2292313fca9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriptions', sa.Column('prodct_id', sa.Integer(), nullable=True))
    op.drop_constraint('subscriptions_proudct_id_fkey', 'subscriptions', type_='foreignkey')
    op.create_foreign_key(None, 'subscriptions', 'products', ['prodct_id'], ['id'])
    op.drop_column('subscriptions', 'proudct_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriptions', sa.Column('proudct_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'subscriptions', type_='foreignkey')
    op.create_foreign_key('subscriptions_proudct_id_fkey', 'subscriptions', 'products', ['proudct_id'], ['id'])
    op.drop_column('subscriptions', 'prodct_id')
    # ### end Alembic commands ###
