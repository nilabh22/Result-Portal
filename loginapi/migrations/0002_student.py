# Generated by Django 4.0.4 on 2022-04-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('department', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=200)),
                ('roll_no', models.IntegerField(max_length=6)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
    ]
