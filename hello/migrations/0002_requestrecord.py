from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("hello", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="RequestRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("when", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("token", models.CharField(max_length=128)),
            ],
        ),
    ]
