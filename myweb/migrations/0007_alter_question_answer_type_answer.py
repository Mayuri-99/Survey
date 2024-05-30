# Generated by Django 5.0.6 on 2024-05-30 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0006_delete_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_type',
            field=models.CharField(choices=[('input', 'Input'), ('textarea', 'Textarea'), ('radio', 'Radio'), ('checkbox', 'Checkbox'), ('range', 'Range')], max_length=10),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myweb.question')),
            ],
        ),
    ]