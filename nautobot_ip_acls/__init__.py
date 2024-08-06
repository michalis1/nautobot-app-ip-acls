"""App declaration for nautobot_ip_acls."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotIPACLsConfig(NautobotAppConfig):
    """App configuration for the nautobot_ip_acls app."""

    name = "nautobot_ip_acls"
    verbose_name = "Nautobot Ip Acls"
    version = __version__
    author = "Michael Milaitis"
    description = "Nautobot Ip Acls."
    base_url = "ip-acls"
    required_settings = []
    min_version = "2.0.1"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}


config = NautobotIPACLsConfig  # pylint:disable=invalid-name
