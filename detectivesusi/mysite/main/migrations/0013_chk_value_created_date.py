# Generated by Django 2.1.7 on 2019-05-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20190512_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='chk_value',
            name='created_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]