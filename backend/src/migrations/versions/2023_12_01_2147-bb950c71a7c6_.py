"""empty message

Revision ID: bb950c71a7c6
Revises: c676b48f0840
Create Date: 2023-12-01 21:47:45.865596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb950c71a7c6'
down_revision: Union[str, None] = 'c676b48f0840'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('total_amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('cart_user_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('cart_pkey')),
    sa.UniqueConstraint('user_id', name=op.f('cart_user_id_key'))
    )
    op.create_index(op.f('cart_id_idx'), 'cart', ['id'], unique=False)
    op.create_table('cart_product',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('cart_id', sa.UUID(), nullable=False),
    sa.Column('count', sa.Integer(), server_default='1', nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], name=op.f('cart_product_cart_id_fkey')),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name=op.f('cart_product_product_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('cart_product_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart_product')
    op.drop_index(op.f('cart_id_idx'), table_name='cart')
    op.drop_table('cart')
    # ### end Alembic commands ###
