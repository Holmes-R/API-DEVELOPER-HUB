# Generated by Django 5.1.3 on 2024-11-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0005_alter_viewer_options_remove_viewer_otp_expiry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewer',
            name='otp_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
