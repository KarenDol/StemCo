# Generated by Django 4.2.7 on 2023-11-14 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Problem",
            fields=[
                (
                    "problem_ID",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                ("content", models.TextField()),
            ],
        ),
    ]