"""Added User.access_level, Project.principal_investigators, PI model

Revision ID: 19ec48af9429
Revises: 4e505a57a151
Create Date: 2018-08-20 14:05:15.955159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19ec48af9429'
down_revision = '4e505a57a151'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('principal_investigator',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=True),
                    sa.Column('email', sa.String(length=64), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('assoc_PI_project',
                    sa.Column('PI_id', sa.Integer(), nullable=True),
                    sa.Column('project_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['PI_id'],
                                            ['principal_investigator.id'], ),
                    sa.ForeignKeyConstraint(['project_id'], ['project.id'], )
                    )
    op.add_column('project', sa.Column('summary',
                  sa.String(length=2048), nullable=True))
    op.add_column('user',
                  sa.Column('access_level', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'access_level')
    op.drop_column('project', 'summary')
    op.drop_table('assoc_PI_project')
    op.drop_table('principal_investigator')
    # ### end Alembic commands ###
