# Generated by Django 5.1.3 on 2024-11-22 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0011_formsubmission_alter_viewerbehaviour_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewer',
            name='email',
            field=models.EmailField(default=' ', max_length=100),
        ),
    ]