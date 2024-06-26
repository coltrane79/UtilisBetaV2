# Generated by Django 4.2.8 on 2024-03-09 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uose', '0006_userregulatorapplicaations_userentitydocuments'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotesEntityDocuments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('private_note', models.BooleanField(default=False)),
                ('note_text', models.TextField()),
                ('note_date', models.DateField()),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uose.entitydocument')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
