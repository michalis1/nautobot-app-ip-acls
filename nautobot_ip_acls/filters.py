from nautobot.apps.filters import (
    BaseFilterSet,
    NaturalKeyOrPKMultipleChoiceFilter,
    NautobotFilterSet,
    SearchFilter,
    TagFilter,
)
from nautobot_ip_acls.models import ACL, ACLEntry

class ACLFilterSet(NautobotFilterSet):
    class Meta:
        model = ACL
        fields = ["identifier"]
    q = SearchFilter(filter_predicates={"identifier": "icontains"})
    tags = TagFilter()

class ACLEntryFilterSet(BaseFilterSet):
    class Meta:
        model = ACLEntry
        fields = ["acl", "sequence_number", "action"]
    q = SearchFilter(
        filter_predicates={"acl__identifier": "icontains"}
    )
    acl = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="identifier", queryset=ACL.objects.all()
    )

