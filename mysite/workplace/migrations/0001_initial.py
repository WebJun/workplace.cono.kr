# Generated by Django 3.2.17 on 2024-03-04 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord_id', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
                ('cookie', models.TextField()),
            ],
        ),
    ]
