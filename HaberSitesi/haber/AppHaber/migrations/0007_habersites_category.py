# Generated by Django 5.0.2 on 2024-03-10 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("AppHaber", "0006_alter_habersites_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="habersites",
            name="category",
            field=models.ManyToManyField(to="AppHaber.category"),
        ),
    ]
