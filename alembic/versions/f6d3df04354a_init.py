"""Init

Revision ID: f6d3df04354a
Revises: 1f014cd5736a
Create Date: 2023-01-13 23:23:24.161557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6d3df04354a'
down_revision = '1f014cd5736a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subjects', sa.Column('teacher_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'subjects', 'teachers', ['teacher_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('teachers_subject_id_fkey', 'teachers', type_='foreignkey')
    op.drop_column('teachers', 'subject_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teachers', sa.Column('subject_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('teachers_subject_id_fkey', 'teachers', 'subjects', ['subject_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'subjects', type_='foreignkey')
    op.drop_column('subjects', 'teacher_id')
    # ### end Alembic commands ###