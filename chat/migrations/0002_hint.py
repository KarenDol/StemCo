# Generated by Django 4.2.7 on 2023-11-16 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hint",
            fields=[
                (
                    "problem_ID",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                ("hint1", models.TextField()),
                ("hint2", models.TextField()),
                ("hint3", models.TextField()),
            ],
        ),
    ]