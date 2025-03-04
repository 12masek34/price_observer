"""cascade product

Revision ID: b7677e951d71
Revises: ce3e47723f60
Create Date: 2025-01-29 13:53:51.188528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7677e951d71'
down_revision: Union[str, None] = 'ce3e47723f60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('subscriptions_product_id_fkey', 'subscriptions', type_='foreignkey')
    op.create_foreign_key(None, 'subscriptions', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subscriptions', type_='foreignkey')
    op.create_foreign_key('subscriptions_product_id_fkey', 'subscriptions', 'products', ['product_id'], ['id'])
    # ### end Alembic commands ###
