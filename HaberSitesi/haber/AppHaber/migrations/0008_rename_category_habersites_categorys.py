# Generated by Django 5.0.2 on 2024-03-11 09:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("AppHaber", "0007_habersites_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="habersites",
            old_name="category",
            new_name="categorys",
        ),
    ]
