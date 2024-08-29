from django.urls import include, path

from nautobot.apps.api import OrderedDefaultRouter
from nautobot_ip_acls.api.views import (
ACLViewSet, ACLEntryViewSet, DeviceIPACLsView
)

router = OrderedDefaultRouter()
router.register("acls", ACLViewSet)
router.register("acl-entries", ACLEntryViewSet)

urlpatterns = [
    path(
        "devices/<uuid:pk>/ip-acls/",
        DeviceIPACLsView.as_view(),
        name="device_ip_acls"
    ),
    path("", include(router.urls)),
]
