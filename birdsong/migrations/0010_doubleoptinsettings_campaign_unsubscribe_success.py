# Generated by Django 3.2.16 on 2022-12-01 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birdsong', '0009_auto_20221129_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='doubleoptinsettings',
            name='campaign_unsubscribe_success',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name='Success page for unsubscription'),
        ),
    ]