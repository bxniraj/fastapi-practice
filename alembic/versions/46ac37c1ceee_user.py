"""user

Revision ID: 46ac37c1ceee
Revises: 31516a4c1dfd
Create Date: 2023-09-25 23:14:36.634693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46ac37c1ceee'
down_revision: Union[str, None] = '31516a4c1dfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('competition_user_id_fkey', 'competition', type_='foreignkey')
    op.create_foreign_key(None, 'competition', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('entry_user_id_fkey', 'entry', type_='foreignkey')
    op.create_foreign_key(None, 'entry', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'entry', type_='foreignkey')
    op.create_foreign_key('entry_user_id_fkey', 'entry', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'competition', type_='foreignkey')
    op.create_foreign_key('competition_user_id_fkey', 'competition', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
