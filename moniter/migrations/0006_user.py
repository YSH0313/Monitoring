# Generated by Django 2.1.1 on 2019-08-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moniter', '0005_data_count_friday'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
            ],
        ),
    ]
