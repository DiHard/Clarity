# Generated by Django 5.0.4 on 2024-04-13 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=250, verbose_name='Полное наименование')),
                ('inn', models.IntegerField(verbose_name='ИНН')),
            ],
            options={
                'verbose_name': 'Юридическое лицо',
                'verbose_name_plural': 'Юридические лица',
            },
        ),
        migrations.CreateModel(
            name='Service_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=250, verbose_name='Название направления оказываемых услуг')),
                ('regular', models.BooleanField(verbose_name='Регулярная услуга, нужно выставлять ежемесячный счет')),
            ],
            options={
                'verbose_name': 'Направление услуги',
                'verbose_name_plural': 'Направление услуг',
            },
        ),
        migrations.CreateModel(
            name='Dogovor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomer_dogovora', models.CharField(max_length=250, verbose_name='Номер договора')),
                ('date_of_signing', models.DateField(verbose_name='Дата начала действия договора')),
                ('contract_completed', models.BooleanField(verbose_name='Договор завершен')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounting.organization')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Accounting.service_type')),
            ],
            options={
                'verbose_name': 'Договор',
                'verbose_name_plural': 'Договоры',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=250, verbose_name='Название оказываемой услуги')),
                ('date_start', models.DateField(verbose_name='Дата начала оказания услуги')),
                ('date_end', models.DateField(verbose_name='Дата окончания оказания услуги')),
                ('price', models.IntegerField(verbose_name='Оплата за услугу')),
                ('payment_made', models.IntegerField(verbose_name='Сумма частичной оплаты счета')),
                ('full_payment', models.BooleanField(verbose_name='Счет полностью оплачен')),
                ('act_approved', models.BooleanField(verbose_name='Акт подписан')),
                ('dogovor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounting.dogovor')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
    ]
