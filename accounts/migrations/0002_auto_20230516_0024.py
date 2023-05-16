# Generated by Django 3.2.18 on 2023-05-15 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold'), ('P', 'Platinum')], max_length=2)),
                ('discount', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='accounts.level'),
        ),
    ]
