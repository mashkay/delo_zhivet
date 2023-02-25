"""phone_number

Revision ID: b34fce67f4a8
Revises: a83d2b2af3e7
Create Date: 2023-02-25 22:03:42.469005

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b34fce67f4a8'
down_revision = 'a83d2b2af3e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('staff',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('login', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('telegram_username', sa.String(length=100), nullable=True),
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('is_banned', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_geospatial_table('assistance_disabled',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('city', sa.Text(), nullable=False),
    sa.Column('full_address', sa.Text(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
    sa.Column('ticketID', sa.Text(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('geometry', Geography(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeogFromText', name='geography'), nullable=True),
    sa.ForeignKeyConstraint(['telegram_id'], ['user.telegram_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('assistance_disabled', schema=None) as batch_op:
        batch_op.create_geospatial_index('idx_assistance_disabled_geometry', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})

    op.create_geospatial_table('pollution',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('photo', sa.String(length=100), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('geometry', Geography(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeogFromText', name='geography'), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
    sa.Column('ticketID', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['telegram_id'], ['user.telegram_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('pollution', schema=None) as batch_op:
        batch_op.create_geospatial_index('idx_pollution_geometry', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})

    op.create_table('roles_users',
    sa.Column('staff_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], )
    )
    op.create_geospatial_table('volunteer',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('full_address', sa.Text(), nullable=False),
    sa.Column('radius', sa.Integer(), nullable=False),
    sa.Column('has_car', sa.Boolean(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('geometry', Geography(geometry_type='POINT', srid=4326, spatial_index=False, from_text='ST_GeogFromText', name='geography'), nullable=True),
    sa.Column('telegram_username', sa.String(length=100), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=13), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_banned', sa.Boolean(), nullable=True),
    sa.Column('ticketID', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['telegram_id'], ['user.telegram_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    with op.batch_alter_table('volunteer', schema=None) as batch_op:
        batch_op.create_geospatial_index('idx_volunteer_geometry', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('volunteer', schema=None) as batch_op:
        batch_op.drop_geospatial_index('idx_volunteer_geometry', postgresql_using='gist', column_name='geometry')

    op.drop_geospatial_table('volunteer')
    op.drop_table('roles_users')
    with op.batch_alter_table('pollution', schema=None) as batch_op:
        batch_op.drop_geospatial_index('idx_pollution_geometry', postgresql_using='gist', column_name='geometry')

    op.drop_geospatial_table('pollution')
    with op.batch_alter_table('assistance_disabled', schema=None) as batch_op:
        batch_op.drop_geospatial_index('idx_assistance_disabled_geometry', postgresql_using='gist', column_name='geometry')

    op.drop_geospatial_table('assistance_disabled')
    op.drop_table('user')
    op.drop_table('staff')
    op.drop_table('role')
    # ### end Alembic commands ###
