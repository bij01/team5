# Generated by Django 3.2.5 on 2022-08-04 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_alter_member_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=60, primary_key=True, serialize=False),
        ),
    ]
