# Generated by Django 2.0.7 on 2018-07-16 05:41

import apps.docks.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookedDock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('po_number', models.CharField(max_length=255)),
                ('truck_number', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Booked Dock',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.docks.models.get_file_path)),
            ],
            options={
                'verbose_name_plural': 'Company',
            },
        ),
        migrations.CreateModel(
            name='Dock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Dock',
            },
        ),
        migrations.CreateModel(
            name='InvitationToUserAndWarehouseAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('token', models.TextField()),
                ('role', models.CharField(choices=[('warehouse', 'Warehouse Admin'), ('general', 'General User')], default='company', max_length=32)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docks.Company')),
            ],
            options={
                'verbose_name_plural': 'Invitation To User And Warehouse Admin',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('open_date', models.TimeField()),
                ('close_date', models.TimeField()),
                ('opened_overnight', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docks.Company')),
            ],
            options={
                'verbose_name_plural': 'Warehouse',
            },
        ),
        migrations.AddField(
            model_name='dock',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docks.Warehouse'),
        ),
        migrations.AddField(
            model_name='bookeddock',
            name='dock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docks.Dock'),
        ),
        migrations.AlterUniqueTogether(
            name='warehouse',
            unique_together={('company', 'name')},
        ),
    ]
