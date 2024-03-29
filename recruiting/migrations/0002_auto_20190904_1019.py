# Generated by Django 2.2.5 on 2019-09-04 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='recruit',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'Age must be a positive number!')]),
        ),
        migrations.AlterField(
            model_name='recruit',
            name='name',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[A-Z][a-z]{2,}$', 'Name must contain only letters (at least 3, 1st - uppercase)', 'invalid_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='recruit',
            unique_together={('planet', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='sith',
            unique_together={('planet', 'name')},
        ),
    ]
