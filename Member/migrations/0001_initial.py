# Generated by Django 3.2.9 on 2021-11-26 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('email', models.AutoField(auto_created=True, db_column='email', primary_key=True, serialize=False)),
                ('phone', models.CharField(db_column='phone', max_length=30, null=True, verbose_name='會員電話')),
                ('name', models.CharField(db_column='name', max_length=160, null=True, verbose_name='會員姓名')),
                ('birthday', models.DateField(db_column='birthday', null=True, verbose_name='會員生日')),
                ('gender', models.IntegerField(choices=[(1, 'male'), (0, 'female')], db_column='gender', null=True, verbose_name='性別')),
                ('address', models.CharField(db_column='address', max_length=255, null=True, verbose_name='會員地址')),
                ('oauthid', models.CharField(db_column='oauthid', max_length=255, null=True, verbose_name='認證ID')),
                ('password', models.CharField(db_column='password', max_length=160, verbose_name='會員密碼')),
            ],
            options={
                'db_table': 'member',
            },
        ),
    ]
