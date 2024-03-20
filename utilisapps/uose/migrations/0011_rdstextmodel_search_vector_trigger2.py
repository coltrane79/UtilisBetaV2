from django.contrib.postgres.search import SearchVector
from django.db import migrations

"""
Version: 1.0.0
Change Log:
- Added search vector trigger for RDSTextModel
- Computed search vector for existing RDSTextModel instances
"""


def compute_search_vector(apps, schema_editor):
    """Compute Search Vector for RDSTextModel

    Args:
        apps (TYPE): Description
        schema_editor (TYPE): Description
    """
    RDSTextModel = apps.get_model("uose", "RDSTextModel")
    RDSTextModel.objects.update(
        search_vector=SearchVector("url", "page_number", "page_text")
    )


class Migration(migrations.Migration):
    """Migration for RDSTextModel Search Vector Trigger"""

    dependencies = [
        ("uose", "0010_userinbox_entity_doc_ref"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE TRIGGER rds_srch_vec_trigger
            BEFORE INSERT OR UPDATE OF url, page_number, page_text
            ON public.uose_rdstextmodel
            FOR EACH ROW
            EXECUTE FUNCTION tsvector_update_trigger('search_vector', 'pg_catalog.english', 'url', 'page_text');
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS rds_srch_vec_trigger
            ON uose_rdstextmodel;
            """,
        ),
    ]

    operations = [
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
