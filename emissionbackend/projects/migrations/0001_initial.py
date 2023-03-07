# Generated by Django 3.2.18 on 2023-03-07 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('day', models.IntegerField(default=1)),
                ('display_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='FormURL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], max_length=2)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.IntegerField(default=1)),
                ('display_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='NotificationMessages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], max_length=2)),
                ('body', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationTitles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], max_length=2)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_fr', models.CharField(max_length=250)),
                ('name_en', models.CharField(max_length=250)),
                ('server_url', models.URLField()),
                ('timezone', models.CharField(choices=[('Montreal', 'America/Montreal'), ('Toronto', 'America/Toronto')], max_length=10)),
                ('daily_forms', models.ManyToManyField(related_name='daily_forms', to='projects.Form')),
                ('daily_notifications', models.ManyToManyField(related_name='daily_notifications', to='projects.Notification')),
                ('main_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_form', to='projects.form')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='messages',
            field=models.ManyToManyField(related_name='notification_messages', to='projects.NotificationMessages'),
        ),
        migrations.AddField(
            model_name='notification',
            name='titles',
            field=models.ManyToManyField(related_name='notification_titles', to='projects.NotificationTitles'),
        ),
        migrations.AddField(
            model_name='form',
            name='urls',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.formurl'),
        ),
    ]
