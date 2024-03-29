# Generated by Django 4.2.8 on 2023-12-18 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("country", models.CharField(max_length=4, unique=True)),
                ("country_name", models.CharField(max_length=250)),
                ("country_iso_code", models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name="Entity",
            fields=[
                (
                    "entity",
                    models.CharField(
                        max_length=4, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("entity_name", models.CharField(max_length=250)),
                ("entity_link", models.URLField()),
                (
                    "entity_country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="uose.country"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EntityDocument",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("link", models.URLField()),
                ("case_number", models.CharField(max_length=100)),
                ("filename_description", models.CharField(max_length=250)),
                ("file_url", models.URLField()),
                ("document_type", models.CharField(max_length=100)),
                ("issued_by_entity_date", models.DateField()),
                ("received_by_entity_date", models.DateField()),
                ("status", models.CharField(max_length=100)),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applicant",
                        to="uose.entity",
                    ),
                ),
                (
                    "entity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entity_ref",
                        to="uose.entity",
                    ),
                ),
                (
                    "submitter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submitter",
                        to="uose.entity",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EntityType",
            fields=[
                (
                    "entity_type",
                    models.CharField(
                        max_length=4, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("entity_type_description", models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name="EntityDocumentMeta",
            fields=[
                (
                    "doc_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="uose.entitydocument",
                        unique=True,
                    ),
                ),
                ("new_doc_indicator", models.BooleanField(default=True)),
                ("content_type", models.CharField(max_length=100)),
                ("content_size", models.IntegerField()),
                ("num_pages", models.IntegerField()),
                ("is_loaded_to_analytics", models.BooleanField(default=False)),
                ("analytics_scrape_date", models.DateField()),
                ("record_insert_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="ProvinceState",
            fields=[
                (
                    "province_state",
                    models.CharField(
                        max_length=4, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("province_state_name", models.CharField(max_length=250)),
                ("province_state_iso_code", models.CharField(max_length=4)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="uose.country"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="entity",
            name="entity_province_state",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="uose.provincestate"
            ),
        ),
        migrations.AddField(
            model_name="entity",
            name="entity_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="uose.entitytype"
            ),
        ),
    ]
