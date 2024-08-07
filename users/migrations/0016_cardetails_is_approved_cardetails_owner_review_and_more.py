# Generated by Django 4.0.1 on 2024-05-24 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_cardetails_remove_saveddetails_vehicle_listing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardetails',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cardetails',
            name='owner_review',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cardetails',
            name='star_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
