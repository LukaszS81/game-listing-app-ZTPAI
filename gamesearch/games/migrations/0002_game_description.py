# Generated by Django 4.2.5 on 2025-04-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
