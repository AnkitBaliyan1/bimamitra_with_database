# Generated by Django 5.0 on 2024-01-02 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application_insure', '0004_delete_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('subject', models.CharField(blank=True, max_length=100)),
                ('message', models.TextField()),
            ],
        ),
    ]
