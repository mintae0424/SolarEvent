# Generated by Django 5.0.2 on 2024-04-17 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revision',
            name='revision_id',
            field=models.IntegerField(unique=True),
        ),
    ]