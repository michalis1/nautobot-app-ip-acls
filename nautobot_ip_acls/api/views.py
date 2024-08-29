from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from nautobot.apps.api import NautobotModelViewSet
from nautobot.dcim.models import Device

from nautobot_ip_acls import filters
from nautobot_ip_acls import models
from nautobot_ip_acls.api import serializers

class DeviceIPACLsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        device = get_object_or_404(Device.objects.restrict(self.request.user, "view"), pk=pk)
        config_context = device.get_config_context()
        return Response({"access_lists": config_context.get("access_lists", {})})

class ACLViewSet(NautobotModelViewSet):
    queryset = models.ACL.objects.all()
    serializer_class = serializers.ACLSerializer
    filterset_class = filters.ACLFilterSet

class ACLEntryViewSet(NautobotModelViewSet):
    queryset = models.ACLEntry.objects.all()
    serializer_class = serializers.ACLEntrySerializer
    filterset_class = filters.ACLEntryFilterSet