# Generated by Django 2.1.7 on 2019-05-12 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20190512_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='search_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('C_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.c_admission')),
                ('ch_val', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.chk_value')),
            ],
        ),
    ]