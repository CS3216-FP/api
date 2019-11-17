"""Add offer responses table

Revision ID: 047af5b48b24
Revises: 8e09e604c7a0
Create Date: 2019-11-17 21:35:35.079956

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "047af5b48b24"
down_revision = "8e09e604c7a0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "offer_responses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("offer_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["offer_id"], ["offers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("offer_responses")
    # ### end Alembic commands ###