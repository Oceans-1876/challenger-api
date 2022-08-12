"""First migration

Revision ID: f9a133b33db1
Revises:
Create Date: 2022-06-26 11:08:18.415909+00:00

"""
import sqlalchemy as sa

from alembic import op
from app.utils.db import Geometry

# revision identifiers, used by Alembic.
revision = "f9a133b33db1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "data_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("title_short", sa.String(length=150), nullable=False),
        sa.Column("curation", sa.String(length=90), nullable=False),
        sa.Column("record_count", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.Date(), nullable=False),
        sa.Column("is_out_link_ready", sa.Boolean(), nullable=False),
        sa.Column("home_url", sa.String(length=200), nullable=True),
        sa.Column("url_template", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_data_sources_id"), "data_sources", ["id"], unique=False)
    op.create_index(
        op.f("ix_data_sources_title"), "data_sources", ["title"], unique=False
    )

    op.create_table(
        "stations",
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("sediment_sample", sa.String(length=50), nullable=True),
        sa.Column(
            "coordinates",
            Geometry(
                geometry_type="POINT",
                srid=4326,
                from_text="ST_GeomFromEWKT",
                name="geometry",
            ),
            nullable=False,
        ),
        sa.Column("location", sa.String(length=200), nullable=False),
        sa.Column("water_body", sa.String(length=200), nullable=False),
        sa.Column("sea_area", sa.String(length=200), nullable=True),
        sa.Column("place", sa.String(length=200), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("fao_area", sa.Integer(), nullable=False),
        sa.Column("gear", sa.String(length=50), nullable=True),
        sa.Column("depth_fathoms", sa.Integer(), nullable=True),
        sa.Column("bottom_water_temp_c", sa.Float(), nullable=True),
        sa.Column("bottom_water_depth_fathoms", sa.Integer(), nullable=True),
        sa.Column("specific_gravity_at_bottom", sa.Float(), nullable=True),
        sa.Column("surface_temp_c", sa.Float(), nullable=True),
        sa.Column("specific_gravity_at_surface", sa.Float(), nullable=True),
        sa.Column("water_temp_c_at_depth_fathoms", sa.JSON(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("hathitrust_urls", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_index(op.f("ix_stations_name"), "stations", ["name"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_full_name"), "users", ["full_name"], unique=False)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "species",
        sa.Column("id", sa.String(length=300), nullable=False),
        sa.Column("record_id", sa.String(length=300), nullable=False),
        sa.Column("current_record_id", sa.String(length=300), nullable=True),
        sa.Column("matched_name", sa.String(length=300), nullable=False),
        sa.Column(
            "matched_canonical_simple_name", sa.String(length=300), nullable=True
        ),
        sa.Column("matched_canonical_full_name", sa.String(length=300), nullable=True),
        sa.Column("current_name", sa.String(length=300), nullable=True),
        sa.Column(
            "current_canonical_simple_name", sa.String(length=300), nullable=True
        ),
        sa.Column("current_canonical_full_name", sa.String(length=300), nullable=True),
        sa.Column("common_name", sa.String(length=300), nullable=True),
        sa.Column("classification_path", sa.String(length=800), nullable=True),
        sa.Column("classification_ranks", sa.String(length=800), nullable=True),
        sa.Column("classification_ids", sa.String(length=800), nullable=True),
        sa.Column("outlink", sa.String(length=300), nullable=True),
        sa.Column("data_source_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["data_source_id"],
            ["data_sources.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_species_current_record_id"),
        "species",
        ["current_record_id"],
        unique=False,
    )
    op.create_index(op.f("ix_species_id"), "species", ["id"], unique=False)
    op.create_index(op.f("ix_species_record_id"), "species", ["record_id"], unique=True)
    op.create_table(
        "species_common_names",
        sa.Column("id", sa.String(length=300), nullable=False),
        sa.Column("language", sa.String(length=300), nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("species_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["species_id"],
            ["species.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_species_common_names_id"), "species_common_names", ["id"], unique=False
    )
    op.create_table(
        "species_extra",
        sa.Column("id", sa.String(length=300), nullable=False),
        sa.Column("scientific_name", sa.String(length=300), nullable=True),
        sa.Column("status", sa.Boolean(), nullable=True),
        sa.Column("unaccepted_reason", sa.Text(), nullable=True),
        sa.Column("valid_name", sa.String(length=300), nullable=False),
        sa.Column("lsid", sa.String(length=300), nullable=True),
        sa.Column("isBrackish", sa.Boolean(), nullable=True),
        sa.Column("isExtinct", sa.Boolean(), nullable=True),
        sa.Column("isFreshwater", sa.Boolean(), nullable=True),
        sa.Column("isMarine", sa.Boolean(), nullable=True),
        sa.Column("isTerrestrial", sa.Boolean(), nullable=True),
        sa.Column("species_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["species_id"],
            ["species.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_species_extra_id"), "species_extra", ["id"], unique=False)
    op.create_table(
        "species_synonyms",
        sa.Column("id", sa.String(length=300), nullable=False),
        sa.Column("scientific_name", sa.String(length=300), nullable=True),
        sa.Column("outlink", sa.String(length=300), nullable=True),
        sa.Column("species_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["species_id"],
            ["species.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_species_synonyms_id"), "species_synonyms", ["id"], unique=False
    )
    op.create_table(
        "stations_species",
        sa.Column("station_id", sa.String(length=20), nullable=False),
        sa.Column("species_id", sa.String(length=300), nullable=False),
        sa.ForeignKeyConstraint(
            ["species_id"],
            ["species.id"],
        ),
        sa.ForeignKeyConstraint(
            ["station_id"],
            ["stations.name"],
        ),
        sa.PrimaryKeyConstraint("station_id", "species_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("stations_species")
    op.drop_index(op.f("ix_species_synonyms_id"), table_name="species_synonyms")
    op.drop_table("species_synonyms")
    op.drop_index(op.f("ix_species_extra_id"), table_name="species_extra")
    op.drop_table("species_extra")
    op.drop_index(op.f("ix_species_common_names_id"), table_name="species_common_names")
    op.drop_table("species_common_names")
    op.drop_index(op.f("ix_species_record_id"), table_name="species")
    op.drop_index(op.f("ix_species_id"), table_name="species")
    op.drop_index(op.f("ix_species_current_record_id"), table_name="species")
    op.drop_table("species")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_full_name"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_stations_name"), table_name="stations")
    op.drop_index(
        "idx_stations_coordinates",
        table_name="stations",
        postgresql_using="gist",
        postgresql_ops={},
    )
    op.drop_table("stations")
    op.drop_index(op.f("ix_data_sources_title"), table_name="data_sources")
    op.drop_index(op.f("ix_data_sources_id"), table_name="data_sources")
    op.drop_table("data_sources")
    # ### end Alembic commands ###
