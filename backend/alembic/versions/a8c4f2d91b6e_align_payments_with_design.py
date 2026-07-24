"""align payments with design

Revision ID: a8c4f2d91b6e
Revises: d7d968499b7a
Create Date: 2026-07-24 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a8c4f2d91b6e"
down_revision: Union[str, Sequence[str], None] = "d7d968499b7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "payments",
        sa.Column(
            "payment_reference",
            sa.String(length=100),
            nullable=True,
        ),
    )
    op.execute(
        "UPDATE payments "
        "SET payment_reference = 'PAY-' || replace(payment_id::text, '-', '') "
        "WHERE payment_reference IS NULL"
    )
    op.alter_column(
        "payments",
        "payment_reference",
        nullable=False,
    )

    op.add_column(
        "payments",
        sa.Column(
            "payment_gateway",
            sa.String(length=50),
            nullable=True,
        ),
    )
    op.alter_column(
        "payments",
        "transaction_reference",
        new_column_name="gateway_transaction_id",
        existing_type=sa.String(length=255),
        existing_nullable=True,
    )
    op.add_column(
        "payments",
        sa.Column(
            "failure_reason",
            sa.Text(),
            nullable=True,
        ),
    )

    op.drop_constraint(
        "ck_payments_amount_non_negative",
        "payments",
        type_="check",
    )
    op.create_check_constraint(
        "ck_payments_amount_positive",
        "payments",
        "amount > 0",
    )
    op.create_check_constraint(
        "ck_payments_payment_method",
        "payments",
        "payment_method IN ('ONLINE', 'COD')",
    )

    op.create_unique_constraint(
        "uq_payments_payment_reference",
        "payments",
        ["payment_reference"],
    )
    op.create_unique_constraint(
        "uq_payments_gateway_transaction_id",
        "payments",
        ["gateway_transaction_id"],
    )
    op.create_index(
        "ix_payments_order_id",
        "payments",
        ["order_id"],
    )
    op.create_index(
        "ix_payments_payment_status",
        "payments",
        ["payment_status"],
    )
    op.create_index(
        "ix_payments_created_at",
        "payments",
        ["created_at"],
    )
    op.create_index(
        "uq_payments_order_success",
        "payments",
        ["order_id"],
        unique=True,
        postgresql_where=sa.text("payment_status = 'SUCCESS'"),
    )

    op.drop_column(
        "payments",
        "updated_at",
    )


def downgrade() -> None:
    op.add_column(
        "payments",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.drop_index(
        "uq_payments_order_success",
        table_name="payments",
        postgresql_where=sa.text("payment_status = 'SUCCESS'"),
    )
    op.drop_index(
        "ix_payments_created_at",
        table_name="payments",
    )
    op.drop_index(
        "ix_payments_payment_status",
        table_name="payments",
    )
    op.drop_index(
        "ix_payments_order_id",
        table_name="payments",
    )
    op.drop_constraint(
        "uq_payments_gateway_transaction_id",
        "payments",
        type_="unique",
    )
    op.drop_constraint(
        "uq_payments_payment_reference",
        "payments",
        type_="unique",
    )
    op.drop_constraint(
        "ck_payments_payment_method",
        "payments",
        type_="check",
    )
    op.drop_constraint(
        "ck_payments_amount_positive",
        "payments",
        type_="check",
    )
    op.create_check_constraint(
        "ck_payments_amount_non_negative",
        "payments",
        "amount >= 0",
    )

    op.drop_column(
        "payments",
        "failure_reason",
    )
    op.alter_column(
        "payments",
        "gateway_transaction_id",
        new_column_name="transaction_reference",
        existing_type=sa.String(length=255),
        existing_nullable=True,
    )
    op.drop_column(
        "payments",
        "payment_gateway",
    )
    op.drop_column(
        "payments",
        "payment_reference",
    )
