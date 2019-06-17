# Generated by Django 2.2.2 on 2019-06-17 08:53

from django.db import migrations, models
import java_wallet.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MultiOut',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('height', models.IntegerField()),
                ('tx_id', java_wallet.fields.PositiveBigIntegerField(db_index=True)),
                ('sender_id', java_wallet.fields.PositiveBigIntegerField(db_index=True)),
                ('recipient_id', java_wallet.fields.PositiveBigIntegerField(db_index=True)),
                ('amount', java_wallet.fields.PositiveBigIntegerField()),
                ('tx_subtype', models.PositiveSmallIntegerField(choices=[(1, 'MultiOut Payment'), (2, 'MultiOutSame Payment')])),
                ('tx_timestamp', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'index_together': {('height', 'tx_timestamp')},
            },
        ),
    ]
