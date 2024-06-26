# Generated by Django 5.0.6 on 2024-05-29 23:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0002_rename_answer_question_answer_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('choice_text', models.CharField(blank=True, max_length=255, null=True)),
                ('Question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.question')),
            ],
        ),
    ]
