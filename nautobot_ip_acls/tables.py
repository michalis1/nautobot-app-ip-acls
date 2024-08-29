import django_tables2
import django_tables2
from nautobot.apps.tables import (
BaseTable, ButtonsColumn, TagColumn, ToggleColumn
)
from nautobot.dcim.models import Device
from nautobot_ip_acls.models import ACL, ACLEntry

class ACLTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = ACL
        fields = ("pk", "identifier", "tags", "actions")
    pk = ToggleColumn()
    identifier = django_tables2.Column(linkify=True)
    tags = TagColumn(url_name="plugins:nautobot_ip_acls:acl_list")
    actions = ButtonsColumn(ACL)

class ACLEntryTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = ACLEntry
        fields = ("pk", "acl", "sequence_number", "prefix", "action",
        "actions")
    pk = ToggleColumn()
    acl = django_tables2.Column(linkify=True)
    sequence_number = django_tables2.Column(linkify=True)
    prefix = django_tables2.Column(linkify=True)
    actions = ButtonsColumn(ACLEntry)

class DeviceAuditTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Device
        fields = ["name", "acl_audit_status"]

    name = django_tables2.Column(linkify=True)
    acl_audit_status = django_tables2.Column(verbose_name="ACL Audit Status", empty_values=(), orderable=False)

    def render_acl_audit_status(self, value, record):
        config_context = record.get_config_context()
        if "access_lists" in config_context and len(config_context["access_lists"]) > 0:
            return "PASSED"
        return "FAILED"
