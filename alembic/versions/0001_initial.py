"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-13 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "monitored_objects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("object_type", sa.String(), nullable=False, server_default="http"),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("check_interval", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("warning_threshold", sa.Float(), nullable=False, server_default="1000"),
        sa.Column("critical_threshold", sa.Float(), nullable=False, server_default="3000"),
        sa.Column("status", sa.String(), nullable=False, server_default="normal"),
        sa.Column("last_checked", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "check_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("object_id", sa.Integer(), sa.ForeignKey("monitored_objects.id"), nullable=False),
        sa.Column("checked_at", sa.DateTime(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("response_time", sa.Float(), nullable=True),
        sa.Column("cpu_load", sa.Float(), nullable=True),
        sa.Column("ram_usage", sa.Float(), nullable=True),
        sa.Column("disk_usage", sa.Float(), nullable=True),
    )

    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("object_id", sa.Integer(), sa.ForeignKey("monitored_objects.id"), nullable=False),
        sa.Column("incident_type", sa.String(), nullable=False),
        sa.Column("severity", sa.String(), nullable=False),
        sa.Column("measured_value", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_seen", sa.DateTime(), nullable=True),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="open"),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("incident_id", sa.Integer(), sa.ForeignKey("incidents.id"), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.Column("channel", sa.String(), nullable=False, server_default="ui"),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column("delivery_status", sa.String(), nullable=False, server_default="sent"),
    )


def downgrade() -> None:
    op.drop_table("notifications")
    op.drop_table("incidents")
    op.drop_table("check_results")
    op.drop_table("monitored_objects")
