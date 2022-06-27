"""create db setup

Revision ID: 43fe9f3727b5
Revises: 
Create Date: 2022-06-27 13:55:41.149694

"""
import time

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43fe9f3727b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    position_table = op.create_table(
        "position",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False)
    )
    users_table = op.create_table(
        "users",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('start_work_from', sa.Float, nullable=False),
        sa.Column('position_key',
                  sa.Integer,
                  sa.ForeignKey('position.id'),
                  server_default="1",
                  ),
        sa.Column('salary', sa.SmallInteger, nullable=False),
        sa.Column('boss',
                  sa.Integer,
                  sa.ForeignKey('users.id'),
                  server_default="1"),
        sa.Column('name', sa.String(50), nullable=False)
    )
    op.bulk_insert(position_table,
                   [
                       {'id': 1, 'name': "admin"}
                   ])
    op.bulk_insert(users_table,
                   [
                       {"start_work_from": time.time(),
                        "salary": 1500,
                        "name": "boss",
                        "position_key": 1
                        }
                   ]
                   )


def downgrade() -> None:
    pass
