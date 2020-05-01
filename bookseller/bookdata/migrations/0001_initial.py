# Generated by Django 3.0.3 on 2020-03-09 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.IntegerField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('catagory_id', models.IntegerField(max_length=10, primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('book_id', models.IntegerField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('year_of_publish', models.CharField(max_length=5)),
                ('price', models.IntegerField(max_length=10)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookdata.Author')),
                ('catagory_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookdata.Catagory')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('publisher_id', models.IntegerField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Orderdetails',
            fields=[
                ('orderno', models.IntegerField(max_length=15, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookdata.Catalog')),
            ],
        ),
        migrations.AddField(
            model_name='catalog',
            name='publisher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookdata.Publisher'),
        ),
    ]
