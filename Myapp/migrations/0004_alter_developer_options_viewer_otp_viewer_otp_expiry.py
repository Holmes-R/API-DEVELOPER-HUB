# Generated by Django 5.1.3 on 2024-11-19 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0003_alter_admin_options_alter_developer_developerid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='developer',
            options={'verbose_name_plural': 'Developers'},
        ),
        migrations.AddField(
            model_name='viewer',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='viewer',
            name='otp_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
