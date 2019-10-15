"""Make BuyOrder round non nullable

Revision ID: 04aa90f6d5f1
Revises: ff31f1d3c98d
Create Date: 2019-10-15 21:57:09.287649

"""
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "04aa90f6d5f1"
down_revision = "ff31f1d3c98d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "buy_orders", "round_id", existing_type=postgresql.UUID(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "buy_orders", "round_id", existing_type=postgresql.UUID(), nullable=True
    )
    # ### end Alembic commands ###
