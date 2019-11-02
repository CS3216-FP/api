"""add bids

Revision ID: 65b3c639b08c
Revises: 550932fd8ea0
Create Date: 2019-11-02 16:30:29.198981

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '65b3c639b08c'
down_revision = '550932fd8ea0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offers',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('chat_room_id', postgresql.UUID(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('number_of_shares', sa.Float(), nullable=False),
    sa.Column('author_id', postgresql.UUID(), nullable=False),
    sa.Column('is_accepted', sa.Boolean(), server_default='f', nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['chat_room_id'], ['chat_rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('offers')
    # ### end Alembic commands ###
