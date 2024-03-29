# Generated by Django 4.2.8 on 2024-03-01 12:56

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uose', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RDSTextModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('page_number', models.IntegerField()),
                ('page_text', models.TextField()),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
            options={
                'indexes': [django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='uose_rdstex_search__2bf063_gin')],
            },
        ),
    ]
