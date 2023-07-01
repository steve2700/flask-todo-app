"""Description of the migration

Revision ID: 1e4e061b6147
Revises: 285026c64bf9
Create Date: 2023-07-01 02:27:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e4e061b6147'
down_revision = '285026c64bf9'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    inspector = sa.inspect(op.get_bind())
    columns = inspector.get_columns(table_name)
    for column in columns:
        if column['name'] == column_name:
            return True
    return False


def upgrade():
    # Add the 'user_id' column to the 'todo' table if it doesn't exist
    if not column_exists('todo', 'user_id'):
        op.add_column('todo', sa.Column('user_id', sa.Integer(), nullable=False, server_default='1'))


def downgrade():
    # Drop the 'user_id' column from the 'todo' table if it exists
    if column_exists('todo', 'user_id'):
        op.drop_column('todo', 'user_id')

