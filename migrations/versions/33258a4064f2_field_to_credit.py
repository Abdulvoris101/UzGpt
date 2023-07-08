"""Field to credit

Revision ID: 33258a4064f2
Revises: df5858be6ab0
Create Date: 2023-07-08 18:32:43.390253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33258a4064f2'
down_revision = 'df5858be6ab0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
    'credit',
        sa.Column('userId', sa.UUID, nullable=False),
    )
    op.create_foreign_key(
        'fk_credit_userId_user',
        'credit',
        'user',
        ['userId'],
        ['id'],
    )



def downgrade() -> None:
    pass
