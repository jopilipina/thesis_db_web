# Generated by Django 2.2.1 on 2019-05-30 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('disease', models.CharField(max_length=50)),
                ('gene', models.CharField(max_length=50)),
                ('relation', models.CharField(max_length=50)),
                ('full_text', models.TextField()),
                ('pmid', models.IntegerField(blank=True, default=None, null=True)),
            ],
            options={
                'unique_together': {('gene', 'relation', 'full_text', 'pmid')},
            },
        ),
    ]
