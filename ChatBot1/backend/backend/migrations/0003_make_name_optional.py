from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_add_name_and_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='CV',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ] 