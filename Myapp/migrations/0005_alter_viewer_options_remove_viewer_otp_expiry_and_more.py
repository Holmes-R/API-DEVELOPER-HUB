# Generated by Django 5.1.3 on 2024-11-19 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0004_alter_developer_options_viewer_otp_viewer_otp_expiry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='viewer',
            options={'verbose_name_plural': 'Viewers'},
        ),
        migrations.RemoveField(
            model_name='viewer',
            name='otp_expiry',
        ),
        migrations.AlterField(
            model_name='viewer',
            name='number',
            field=models.BigIntegerField(unique=True),
        ),
    ]
