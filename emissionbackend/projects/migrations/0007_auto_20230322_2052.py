# Generated by Django 3.2.18 on 2023-03-22 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20230320_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('fr', 'Francais'), ('en', 'English')], max_length=2)),
                ('value', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='mode',
            old_name='mode_translations',
            new_name='texts',
        ),
        migrations.RenameField(
            model_name='purpose',
            old_name='purpose_translations',
            new_name='texts',
        ),
        migrations.AddField(
            model_name='mode',
            name='label',
            field=models.CharField(default='Montreal', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purpose',
            name='label',
            field=models.CharField(default='Montreal', max_length=250),
            preserve_default=False,
        ),
    ]
