"""init

Revision ID: 25e8a7b480f0
Revises: 
Create Date: 2023-07-18 09:42:05.007673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25e8a7b480f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coupons',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('coupon_code', sa.String(length=6), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.Column('max_utilizations', sa.SmallInteger(), nullable=False),
    sa.Column('min_purchase_value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('discount_type', sa.String(length=20), nullable=False),
    sa.Column('discount_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('is_general_public', sa.Boolean(), nullable=False),
    sa.Column('valid_first_purchase', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('coupon_code')
    )
    op.create_table('coupons_utilizations',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('utilization_date', sa.DateTime(), nullable=False),
    sa.Column('coupon_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['coupon_id'], ['coupons.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('coupons_utilizations')
    op.drop_table('coupons')
    # ### end Alembic commands ###
