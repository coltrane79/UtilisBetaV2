# Generated by Django 4.2.8 on 2024-03-08 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uose', '0004_regulatorapplicaations'),
    ]

    operations = [
        migrations.AddField(
            model_name='regulatorapplicaations',
            name='appl_category',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='regulatorapplicaations',
            name='applicant',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='regulatorapplicaations',
            name='market_type',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]
