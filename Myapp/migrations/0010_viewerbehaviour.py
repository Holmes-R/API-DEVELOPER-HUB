# Generated by Django 5.1.3 on 2024-11-22 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0009_viewer_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewerBehaviour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=50)),
                ('api_name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.viewer')),
            ],
        ),
    ]