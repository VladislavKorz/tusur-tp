# Generated by Django 4.1.4 on 2022-12-10 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_card_profile_specialization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup_profile',
            name='ceo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Организатор'),
        ),
        migrations.AddField(
            model_name='team',
            name='role',
            field=models.CharField(max_length=50, null=True, verbose_name='Роль в стартапе'),
        ),
    ]