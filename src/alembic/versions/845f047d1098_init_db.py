"""init_db

Revision ID: 845f047d1098
Revises: 
Create Date: 2024-06-11 17:46:29.717997

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from src.core.security import get_password_hash

# revision identifiers, used by Alembic.
revision: str = '845f047d1098'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=50),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
                    sa.UniqueConstraint('name', name='roles_name_key')
                    )
    op.execute("INSERT INTO roles VALUES (1, 'admin'), (2, 'viewer')")
    op.create_table('users',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=50),
                              autoincrement=False, nullable=False),
                    sa.Column('email', sa.VARCHAR(length=100),
                              autoincrement=False, nullable=False),
                    sa.Column('full_name', sa.VARCHAR(length=100),
                              autoincrement=False, nullable=True),
                    sa.Column('hashed_password', sa.CHAR(length=60),
                              autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
                    sa.Column('role_id', sa.INTEGER(),
                              autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], [
                        'roles.id'], name='users_role_id_fkey', onupdate='CASCADE', ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('id', name='users_pkey'),
                    sa.UniqueConstraint('email', name='users_email_key'),
                    sa.UniqueConstraint('username', name='users_username_key')
                    )
    # Create default admin and user
    # !!! Password is not secure!!!
    op.execute(f"""
INSERT INTO users (username, email, full_name, hashed_password, role_id)
 VALUES ('admin', 'admin@mail.com', 'Default, Admin', '{get_password_hash('admin')}', (SELECT id FROM roles WHERE name = 'admin'))
""")
    op.execute(f"""
INSERT INTO users (username, email, full_name, hashed_password, role_id)
 VALUES ('user', 'user@mail.com', 'Default User', '{get_password_hash('user')}', (SELECT id FROM roles WHERE name = 'viewer'))
""")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
