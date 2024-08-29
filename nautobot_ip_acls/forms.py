from django import forms

from nautobot.apps.forms import (
BootstrapMixin, NautobotModelForm, DynamicModelChoiceField
)
from nautobot.ipam.models import Prefix
from nautobot_ip_acls.models import ACL, ACLEntry

class ACLForm(NautobotModelForm):
    class Meta:
        model = ACL
        fields = ["identifier"]

class ACLEntryForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = ACLEntry
        fields = ["acl", "sequence_number", "prefix", "action"]
    acl = DynamicModelChoiceField(
        queryset=ACL.objects.all(), label="ACL"
    )
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(), required=False
    )
