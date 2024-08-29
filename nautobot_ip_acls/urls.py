from django.urls import path
from nautobot.apps.urls import NautobotUIViewSetRouter

from nautobot_ip_acls import views

app_name = "nautobot_ip_acls"
router = NautobotUIViewSetRouter()
router.register("acls", views.ACLUIViewSet)
router.register("acl-entries", views.ACLEntryUIViewSet)
router.register("devices", views.DeviceIPACLsAuditViewSet)
                
urlpatterns = [
    path(
        "devices/<uuid:pk>/ip-acls/",
        views.DeviceIPACLsView.as_view(),
        name="device_ip_acls",
    ),
]
urlpatterns += router.urls
