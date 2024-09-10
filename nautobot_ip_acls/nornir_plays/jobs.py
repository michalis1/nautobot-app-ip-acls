from nautobot.apps.jobs import Job, MultiObjectVar
from nautobot.dcim.models import Device

from nautobot_ip_acls.nornir_plays.get_device_info import get_device_info

name = "Nornir Jobs"

class GetDeviceInfo(Job):

    selected_devices = MultiObjectVar(
        label="Devices",
        description="Devices to get info",
        model=Device,
    )

    class Meta:
        """Metadata describing this job."""

        name = "Get Device Info"
        has_sensitive_variables = False

    def run(self, selected_devices):
        devices = selected_devices
        get_device_info(self, devices)