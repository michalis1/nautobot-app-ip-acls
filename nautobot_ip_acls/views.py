from nautobot.apps import views
from nautobot.dcim.models import Device
from nautobot.dcim.filters import DeviceFilterSet

from nautobot_ip_acls import forms, filters, models, tables
from nautobot_ip_acls.api import serializers
from nautobot_ip_acls.tables import DeviceAuditTable

class ACLUIViewSet(views.NautobotUIViewSet):
    filterset_class = filters.ACLFilterSet
    form_class = forms.ACLForm
    lookup_field = "pk"
    queryset = models.ACL.objects.all()
    serializer_class = serializers.ACLSerializer
    table_class = tables.ACLTable

class ACLEntryUIViewSet(views.NautobotUIViewSet):
    filterset_class = filters.ACLEntryFilterSet
    form_class = forms.ACLEntryForm
    lookup_field = "pk"
    queryset = models.ACLEntry.objects.all()
    serializer_class = serializers.ACLEntrySerializer
    table_class = tables.ACLEntryTable

class DeviceIPACLsView(views.ObjectView):
    queryset = Device.objects.all()
    template_name = "nautobot_ip_acls/device_ip_acls.html"

    def get_extra_context(self, request, instance):
        return {"config_context": instance.get_config_context()}


class DeviceIPACLsAuditViewSet(views.ObjectListViewMixin):
    queryset = Device.objects.all()
    filterset_class = DeviceFilterSet
    table_class = DeviceAuditTable
