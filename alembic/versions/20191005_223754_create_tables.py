"""Create tables

Revision ID: 62f5dd3d2be2
Revises: 
Create Date: 2019-10-05 22:37:54.440190

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "62f5dd3d2be2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "buyers",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sellers",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "buy_orders",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("buyer_id", postgresql.UUID(), nullable=True),
        sa.Column("number_of_shares", sa.Float(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["buyer_id"], ["buyers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "invites",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("origin_seller_id", postgresql.UUID(), nullable=True),
        sa.Column("destination_email", sa.String(), nullable=True),
        sa.Column("valid", sa.Boolean(), nullable=True),
        sa.Column("expiry_time", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["origin_seller_id"], ["sellers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sell_orders",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("seller_id", postgresql.UUID(), nullable=True),
        sa.Column("number_of_shares", sa.Float(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["seller_id"], ["sellers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "matches",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("buy_order_id", postgresql.UUID(), nullable=True),
        sa.Column("sell_order_id", postgresql.UUID(), nullable=True),
        sa.Column("number_of_shares", sa.Float(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["buy_order_id"], ["buy_orders.id"]),
        sa.ForeignKeyConstraint(["sell_order_id"], ["sell_orders.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("matches")
    op.drop_table("sell_orders")
    op.drop_table("invites")
    op.drop_table("buy_orders")
    op.drop_table("sellers")
    op.drop_table("buyers")
    # ### end Alembic commands ###