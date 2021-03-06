# Generated by Django 2.2.8 on 2020-01-07 01:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kyykka', '0009_auto_20190402_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='abbreviation',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='throw',
            name='score_first',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='throw',
            name='score_fourth',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='throw',
            name='score_second',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='throw',
            name='score_third',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
