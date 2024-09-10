from nautobot.apps.jobs import register_jobs

from nautobot_ip_acls.ssot.jobs import ExampleYAMLDataSource
from nautobot_ip_acls.nornir_plays.jobs import GetDeviceInfo

# Expose jobs to Nautobot
jobs = [ExampleYAMLDataSource, GetDeviceInfo]

register_jobs(*jobs)
