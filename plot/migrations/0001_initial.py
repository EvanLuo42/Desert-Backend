# Generated by Django 4.0.3 on 2022-04-11 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('chapter_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('chapter_name', models.CharField(max_length=255)),
                ('plot_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ChapterUnlock',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('chapter_id', models.IntegerField(null=True)),
                ('user_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('plot_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('plot_content', models.TextField()),
                ('plot_title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PlotRead',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('plot_id', models.IntegerField(null=True)),
                ('user_id', models.IntegerField(null=True)),
            ],
        ),
    ]
