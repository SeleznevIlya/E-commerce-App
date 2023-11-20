"""add Product, Category and ProductCategory models

Revision ID: c676b48f0840
Revises: d2f89b22d68c
Create Date: 2023-11-20 20:46:03.947726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c676b48f0840'
down_revision: Union[str, None] = 'd2f89b22d68c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('category_name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('category_pkey'))
    )
    op.create_index(op.f('category_id_idx'), 'category', ['id'], unique=False)
    op.create_table('product',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('product_name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), server_default='', nullable=False),
    sa.Column('product_code', sa.String(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('product_pkey'))
    )
    op.create_index(op.f('product_id_idx'), 'product', ['id'], unique=False)
    op.create_index(op.f('product_product_name_idx'), 'product', ['product_name'], unique=True)
    op.create_table('product_category',
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('category_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name=op.f('product_category_category_id_fkey')),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name=op.f('product_category_product_id_fkey')),
    sa.PrimaryKeyConstraint('product_id', 'category_id', name=op.f('product_category_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_category')
    op.drop_index(op.f('product_product_name_idx'), table_name='product')
    op.drop_index(op.f('product_id_idx'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('category_id_idx'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
