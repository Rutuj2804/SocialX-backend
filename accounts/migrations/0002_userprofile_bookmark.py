# Generated by Django 3.2 on 2021-05-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bookmark',
            field=models.ManyToManyField(related_name='bookmark', to='posts.Post'),
        ),
    ]