# Generated by Django 2.2.2 on 2019-06-20 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guestbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=1000)),
                ('regdate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
