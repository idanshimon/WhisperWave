"""Initial migration

Revision ID: 67bffe2f125b
Revises: 
Create Date: 2024-09-06 13:23:48.064435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67bffe2f125b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_metadata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=120), nullable=False),
    sa.Column('file_type', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('upload_timestamp', sa.DateTime(), nullable=True),
    sa.Column('transcription_text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file_metadata')
    # ### end Alembic commands ###
