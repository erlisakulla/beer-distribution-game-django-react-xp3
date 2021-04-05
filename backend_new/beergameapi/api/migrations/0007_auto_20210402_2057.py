# Generated by Django 3.1.7 on 2021-04-02 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210402_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='downstreamPlayer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_downstreamPlayer', to='api.role'),
        ),
        migrations.AlterField(
            model_name='role',
            name='playedBy',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_instructor': False}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='role',
            name='upstreamPlayer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_upstreamPlayer', to='api.role'),
        ),
        migrations.AlterField(
            model_name='week',
            name='backlog',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='week',
            name='demand',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='week',
            name='incoming_shipment',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='week',
            name='inventory',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='week',
            name='order_placed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='week',
            name='outgoing_shipment',
            field=models.IntegerField(default=0),
        ),
    ]