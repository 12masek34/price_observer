"""parse error count

Revision ID: e9230f7cd18c
Revises: b7677e951d71
Create Date: 2025-03-12 14:03:44.494724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9230f7cd18c'
down_revision: Union[str, None] = 'b7677e951d71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriptions', sa.Column('parse_error_count', sa.Integer(), nullable=False, server_defaul=0))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscriptions', 'parse_error_count')
    # ### end Alembic commands ###
