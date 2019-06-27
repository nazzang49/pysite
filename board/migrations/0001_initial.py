# Generated by Django 2.2.2 on 2019-06-21 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=2000)),
                ('hit', models.IntegerField(default=0)),
                ('regdate', models.DateTimeField(auto_now=True)),
                ('groupno', models.IntegerField(default=0)),
                ('orderno', models.IntegerField(default=0)),
                ('depth', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]
