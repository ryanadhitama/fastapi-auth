"""Create table users

Revision ID: 1f3d4caea618
Revises: 
Create Date: 2024-03-30 00:32:32.643792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f3d4caea618'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER, nullable=False),
        sa.Column("name", sa.VARCHAR(100), nullable=False),
        sa.Column("email", sa.VARCHAR(100), nullable=False),
        sa.Column("password", sa.VARCHAR(100), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            nullable=True,
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass