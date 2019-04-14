# Generated by Django 2.1.7 on 2019-04-14 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20190407_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='chk_value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferwhere1', models.IntegerField(blank=True, null=True)),
                ('preferwhere2', models.IntegerField(blank=True, null=True)),
                ('preferwhere3', models.IntegerField(blank=True, null=True)),
                ('prefertype1', models.IntegerField(blank=True, null=True)),
                ('prefertype2', models.IntegerField(blank=True, null=True)),
                ('prefertype3', models.IntegerField(blank=True, null=True)),
                ('prefertype4', models.IntegerField(blank=True, null=True)),
                ('prefertype5', models.IntegerField(blank=True, null=True)),
                ('prefertype6', models.IntegerField(blank=True, null=True)),
                ('prefertype7', models.IntegerField(blank=True, null=True)),
                ('total_avgrate', models.FloatField(blank=True, null=True)),
                ('main_avgrate', models.FloatField(blank=True, null=True)),
                ('executive_cnt', models.IntegerField(blank=True, null=True)),
                ('absent', models.IntegerField(blank=True, null=True)),
                ('award_cnt', models.IntegerField(blank=True, null=True)),
                ('circle_cnt', models.IntegerField(blank=True, null=True)),
                ('volunteer', models.IntegerField(blank=True, null=True)),
                ('reading', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
