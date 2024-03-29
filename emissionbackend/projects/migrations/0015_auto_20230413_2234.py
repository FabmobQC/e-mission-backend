# Generated by Django 3.2.18 on 2023-04-13 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_alter_email_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnInstallNotification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('delay', models.IntegerField(default=1)),
                ('delay_unit', models.CharField(max_length=30)),
                ('messages', models.ManyToManyField(related_name='on_install_notification_messages', to='projects.NotificationMessages')),
                ('titles', models.ManyToManyField(related_name='on_install_notification_titles', to='projects.NotificationTitles')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='on_install_notifications',
            field=models.ManyToManyField(blank=True, related_name='on_install_notifications', to='projects.OnInstallNotification'),
        ),
    ]
