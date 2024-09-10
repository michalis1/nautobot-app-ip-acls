import os

import yaml
from diffsync import DiffSync

from nautobot_ssot.contrib import NautobotAdapter

from nautobot_ip_acls.ssot.models import PrefixModel, VRFModel, IPAddressModel

#####
# Defining Nautobot Adapter
#####
class ExampleNautobotAdapter(NautobotAdapter):
    """DiffSync adapter for Nautobot."""

    vrf = VRFModel
    prefix = PrefixModel
    ip_address = IPAddressModel
    top_level = (
        "prefix",
        "ip_address",
        "vrf",
    )


#####
# Defining Remote YAML Adapter
#####
class ExampleRemoteAdapter(DiffSync):
    """DiffSync adapter for remote system."""

    vrf = VRFModel
    prefix = PrefixModel
    ip_address = IPAddressModel
    top_level = (
        "prefix",
        "ip_address",
        "vrf",
    )

    def load(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "example.yaml")) as yaml_content:
            data = yaml.safe_load(yaml_content)

        for prefix in data["prefixes"]:
            network, prefix_length = prefix["prefix"].split("/")
            loaded_prefix = self.prefix(
                network=network,
                prefix_length=int(prefix_length),
                vrf_name=prefix["virtual_routing_instance"],
            )
            self.add(loaded_prefix)
            if ip_addresses:=prefix.get("ip_addresses"):
                for ip_address in ip_addresses:
                    host, mask_length = ip_address.split("/")
                    loaded_ip = self.ip_address(
                        host = host,
                        mask_length = mask_length
                    )
                    self.add(loaded_ip)
                    # loaded_prefix.add_child(loaded_ip)


        for vrf in data["virtual_routing_instances"]:
            prefixes = []
            for prefix in self.get_all("prefix"):
                if prefix.vrf_name == vrf["name"]:
                    prefixes.append(
                        {
                            "network": prefix.network,
                            "prefix_length": prefix.prefix_length,
                        }
                    )
            loaded_vrf = self.vrf(
                name=vrf["name"],
                rd=vrf["route_distinguisher"],
                description=vrf["comments"],
                prefixes=prefixes,
            )
            self.add(loaded_vrf)
