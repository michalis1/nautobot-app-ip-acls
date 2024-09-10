
from typing import Optional, List

try:
    from typing import TypedDict  # Python>=3.9
except ImportError:
    from typing_extensions import TypedDict  # Python<3.9

from nautobot.ipam.models import VRF, Prefix, IPAddress

from nautobot_ssot.contrib import NautobotModel

name = "An SSoT Example"

#####
# Defining Data Models
#####
class PrefixModel(NautobotModel):
    """Prefix Model for DiffSync."""

    _model = Prefix
    _modelname = "prefix"
    _identifiers = ("network", "prefix_length", "namespace__name")
    _attributes = ("status__name", "type")
    # _children = {"ip_address": "ip_addresses"} # The key should be the model_name of the child

    network: str
    type: str = "network"
    namespace__name: str = "Global"
    prefix_length: int
    status__name: str = "Active"
    vrf_name: Optional[str] = None
    # ip_addresses: List["IPAddressModel"] = []

    # def get_children(self):
    #     return {
    #         "ip_address": self.get_all_children_for_model("ip_address")
    #     }

class IPAddressModel(NautobotModel):
    """Prefix Model for DiffSync."""

    _model = IPAddress
    _modelname = "ip_address"
    _identifiers = ("host", "mask_length")
    _attributes = ("status__name", "type")

    host: str
    mask_length: int
    type: str = "host"
    status__name: str = "Active"

class PrefixDict(TypedDict):
    """This typed dict is 100% decoupled from the `NautobotPrefix`
    class defined above, and used to be referenced in a Many-to-many
    relationship."""

    network: str
    prefix_length: int


class VRFModel(NautobotModel):
    """VRF Model for DiffSync."""

    _model = VRF
    _modelname = "vrf"
    _identifiers = ("name", "namespace__name")
    _attributes = ("rd", "description", "prefixes")

    name: str
    namespace__name: str = "Global"
    rd: Optional[str]
    description: Optional[str]
    prefixes: List[PrefixDict] = []