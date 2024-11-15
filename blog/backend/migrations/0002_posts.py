# Generated by Django 4.1.5 on 2024-11-15 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=45)),
                ('title', models.CharField(blank=True, max_length=405, null=True)),
                ('description', models.CharField(blank=True, max_length=405, null=True)),
                ('tags', models.CharField(blank=True, max_length=450, null=True)),
                ('date', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'posts',
                'managed': False,
            },
        ),
    ]
