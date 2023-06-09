# Generated by Django 4.1.4 on 2022-12-10 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_profile_secret_link_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='startup_profile',
            options={'verbose_name': 'Стартап', 'verbose_name_plural': 'Стартапы'},
        ),
        migrations.CreateModel(
            name='DatingCard_StartUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_start_up', models.BooleanField(default=False, verbose_name='Стартап лайкунл профиль')),
                ('match_profile', models.BooleanField(default=False, verbose_name='Профиль лайкунл стартап')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.card_profile', verbose_name='Пользователь')),
                ('start_up', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.startup_profile', verbose_name='Стартап проект')),
            ],
        ),
    ]
