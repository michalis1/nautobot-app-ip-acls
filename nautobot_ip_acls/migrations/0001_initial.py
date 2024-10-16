# Generated by Django 3.2.25 on 2024-08-27 08:44

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import nautobot.core.models.fields
import nautobot.extras.models.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0108_jobbutton_enabled'),
        ('ipam', '0046_update_all_charfields_max_length_to_255'),
    ]

    operations = [
        migrations.CreateModel(
            name='ACL',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('identifier', models.CharField(max_length=255, unique=True)),
                ('tags', nautobot.core.models.fields.TagsField(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'ACL',
            },
            bases=(models.Model, nautobot.extras.models.mixins.DynamicGroupMixin, nautobot.extras.models.mixins.NotesMixin),
        ),
        migrations.CreateModel(
            name='ACLEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('sequence_number', models.PositiveSmallIntegerField()),
                ('action', models.CharField(max_length=10)),
                ('acl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nautobot_ip_acls.acl')),
                ('prefix', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipam.prefix')),
            ],
            options={
                'verbose_name': 'ACL entry',
                'verbose_name_plural': 'ACL entries',
                'ordering': ('acl__identifier', 'sequence_number'),
                'unique_together': {('acl', 'sequence_number')},
            },
        ),
    ]
