"""add tiktok submission and moderation

Revision ID: dd44aa20854e
Revises: de84c6b4d3cd
Create Date: 2026-08-17 12:18:58.052909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd44aa20854e'
down_revision = 'de84c6b4d3cd'
branch_labels = None
depends_on = None


def upgrade():

    # ============================================================
    # CHALLENGE SUBMISSIONS
    # ============================================================

    with op.batch_alter_table(
        'challenge_submissions',
        schema=None
    ) as batch_op:

        # TikTok video URL
        batch_op.add_column(
            sa.Column(
                'tiktok_url',
                sa.String(length=500),
                nullable=True
            )
        )

        # Existing submissions must be approved because they
        # existed before moderation was introduced.
        batch_op.add_column(
            sa.Column(
                'status',
                sa.String(length=20),
                nullable=False,
                server_default='approved'
            )
        )

        # Optional admin moderation explanation
        batch_op.add_column(
            sa.Column(
                'moderation_note',
                sa.Text(),
                nullable=True
            )
        )

        # Index for quickly finding pending submissions
        batch_op.create_index(
            batch_op.f('ix_challenge_submissions_status'),
            ['status'],
            unique=False
        )

    # ============================================================
    # CHALLENGE VOTES
    # ============================================================

    with op.batch_alter_table(
        'challenge_votes',
        schema=None
    ) as batch_op:

        batch_op.drop_constraint(
            batch_op.f('unique_user_submission_vote'),
            type_='unique'
        )


def downgrade():

    # ============================================================
    # CHALLENGE VOTES
    # ============================================================

    with op.batch_alter_table(
        'challenge_votes',
        schema=None
    ) as batch_op:

        batch_op.create_unique_constraint(
            batch_op.f('unique_user_submission_vote'),
            [
                'submission_id',
                'user_id'
            ],
            postgresql_nulls_not_distinct=False
        )

    # ============================================================
    # CHALLENGE SUBMISSIONS
    # ============================================================

    with op.batch_alter_table(
        'challenge_submissions',
        schema=None
    ) as batch_op:

        batch_op.drop_index(
            batch_op.f(
                'ix_challenge_submissions_status'
            )
        )

        batch_op.drop_column(
            'moderation_note'
        )

        batch_op.drop_column(
            'status'
        )

        batch_op.drop_column(
            'tiktok_url'
        )