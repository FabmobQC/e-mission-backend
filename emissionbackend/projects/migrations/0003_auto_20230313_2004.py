# Generated by Django 3.2.18 on 2023-03-13 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20230307_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMessages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], max_length=2)),
                ('body', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EmailSubjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], max_length=2)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ModeTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], max_length=2)),
                ('value', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PurposeTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], max_length=2)),
                ('value', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='daily_forms',
            field=models.ManyToManyField(blank=True, null=True, related_name='daily_forms', to='projects.Form'),
        ),
        migrations.AlterField(
            model_name='project',
            name='daily_notifications',
            field=models.ManyToManyField(blank=True, null=True, related_name='daily_notifications', to='projects.Notification'),
        ),
        migrations.AlterField(
            model_name='project',
            name='main_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_form', to='projects.form'),
        ),
        migrations.CreateModel(
            name='Purpose',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('purpose_translations', models.ManyToManyField(related_name='purpose_translations', to='projects.PurposeTranslation')),
            ],
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mode_translations', models.ManyToManyField(related_name='mode_translations', to='projects.ModeTranslation')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.IntegerField(default=1)),
                ('display_time', models.TimeField()),
                ('messages', models.ManyToManyField(related_name='notification_messages', to='projects.EmailMessages')),
                ('subjects', models.ManyToManyField(related_name='notification_titles', to='projects.EmailSubjects')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='daily_emails',
            field=models.ManyToManyField(blank=True, null=True, related_name='daily_emails', to='projects.Email'),
        ),
        migrations.AddField(
            model_name='project',
            name='modes',
            field=models.ManyToManyField(blank=True, null=True, to='projects.Mode'),
        ),
        migrations.AddField(
            model_name='project',
            name='purposes',
            field=models.ManyToManyField(blank=True, null=True, to='projects.Purpose'),
        ),
    ]
