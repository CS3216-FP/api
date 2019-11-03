"""add offer

Revision ID: 33a3423b63e1
Revises: ce35232971d0
Create Date: 2019-11-03 12:51:44.618178

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "33a3423b63e1"
down_revision = "ce35232971d0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "offers",
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
        sa.Column("chat_room_id", postgresql.UUID(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("number_of_shares", sa.Float(), nullable=False),
        sa.Column("author_id", postgresql.UUID(), nullable=False),
        sa.Column("is_agreeable", sa.Boolean(), server_default="f", nullable=False),
        sa.Column("is_rejected", sa.Boolean(), server_default="f", nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["chat_room_id"], ["chat_rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("offers")
    # ### end Alembic commands ###