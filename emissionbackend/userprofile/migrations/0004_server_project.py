# Generated by Django 3.2.18 on 2023-10-10 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20230413_2234'),
        ('userprofile', '0003_alter_user_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
