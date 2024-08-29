from rest_framework import serializers
from nautobot.apps.api import (
NautobotModelSerializer, TaggedModelSerializerMixin
)
from nautobot_ip_acls.models import ACL, ACLEntry

class ACLSerializer(
NautobotModelSerializer, TaggedModelSerializerMixin
):
    class Meta:
        model = ACL
        fields = ["__all__"]
        
class ACLEntrySerializer(NautobotModelSerializer):
    class Meta:
        model = ACLEntry
        fields = ["__all__"]