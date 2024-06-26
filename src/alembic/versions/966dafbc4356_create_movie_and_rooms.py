"""create_movie_and_rooms

Revision ID: 966dafbc4356
Revises: 845f047d1098
Create Date: 2024-06-11 20:00:52.254841

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '966dafbc4356'
down_revision: Union[str, None] = '845f047d1098'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room_types',
                    sa.Column('id', sa.INTEGER(), autoincrement=True,
                              nullable=False, unique=True),
                    sa.Column('name', sa.VARCHAR(length=50),
                              autoincrement=False, nullable=False, unique=True),
                    )
    op.execute(
        "INSERT INTO room_types VALUES (1, 'open_space'), (2, 'fixed_seats')")
    op.create_table('rooms',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=50),
                              autoincrement=False, nullable=False),
                    sa.Column('type', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.Column('capacity', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='rooms_pkey'),
                    sa.ForeignKeyConstraint(['type'], [
                        'room_types.id'], name='room_type_id_fkey', onupdate='CASCADE', ondelete='CASCADE'),
                    )
    op.create_table('seats',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('room_id', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.Column('row', sa.VARCHAR(length=1),
                              autoincrement=False, nullable=False),
                    sa.Column('number', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='seats_pkey'),
                    sa.ForeignKeyConstraint(['room_id'], [
                        'rooms.id'], name='seats_room_id_fkey', onupdate='CASCADE', ondelete='CASCADE'),
                    )
    op.create_table('movies',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=50),
                              autoincrement=False, nullable=False),
                    sa.Column('duration_minutes', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='movies_pkey'),
                    )
    # Fill DB with some data
    op.execute(
        "INSERT INTO rooms VALUES (1, 'Room 1', 2, 20), (2, 'Room 2', 1, 10)")
    op.execute("""
        INSERT INTO seats VALUES 
            (1, 1, 'A', 1), (2, 1, 'A', 2),
            (3, 1, 'A', 3), (4, 1, 'A', 4),
            (5, 1, 'A', 5), (6, 1, 'A', 6),
            (7, 1, 'A', 7), (8, 1 ,'A', 8),
            (9, 1, 'A', 9), (10, 1, 'A', 10),
            (11, 1, 'B', 1), (12, 1, 'B', 2),
            (13, 1, 'B', 3), (14, 1, 'B', 4),
            (15, 1, 'B', 5), (16, 1, 'B', 6),
            (17, 1, 'B', 7), (18, 1, 'B', 8),
            (19, 1, 'B', 9), (20, 1, 'B', 10)
        """)
    op.execute("INSERT INTO movies VALUES (1, 'Dune', 180), (2, 'Tenet', 150)")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    op.drop_table('seats')
    op.drop_table('rooms')
    op.drop_table('room_types')
    # ### end Alembic commands ###
