"""add coupon fields to carts

Revision ID: d7d968499b7a
Revises: f1bc98e0cc6a
Create Date: 2026-07-20 20:36:04.784787

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d7d968499b7a"
down_revision: Union[str, Sequence[str], None] = "f1bc98e0cc6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "carts",
        sa.Column(
            "applied_coupon_code",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "carts",
        sa.Column(
            "discount_amount",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="0.00",
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "carts",
        "discount_amount",
    )

    op.drop_column(
        "carts",
        "applied_coupon_code",
    )
