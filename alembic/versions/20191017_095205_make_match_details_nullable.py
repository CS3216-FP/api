"""Make Match details nullable

Revision ID: 6fb9fbed5f20
Revises: 04aa90f6d5f1
Create Date: 2019-10-17 09:52:05.886003

"""
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "6fb9fbed5f20"
down_revision = "04aa90f6d5f1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "matches",
        "number_of_shares",
        existing_type=postgresql.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    op.alter_column(
        "matches",
        "price",
        existing_type=postgresql.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "matches",
        "price",
        existing_type=postgresql.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.alter_column(
        "matches",
        "number_of_shares",
        existing_type=postgresql.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    # ### end Alembic commands ###