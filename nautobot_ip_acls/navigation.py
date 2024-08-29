"""Module to change nautobot navigation menu."""

from nautobot.apps.ui import NavMenuGroup, NavMenuItem, NavMenuTab

menu_items = (
    NavMenuTab(
        name="IP ACLs",
        weight=1000,
        groups=(
            NavMenuGroup(
                name="ACLs",
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_ip_acls:acl_list",
                        name="ACLs",
                        permissions=["nautobot_ip_acls.view_acl"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_ip_acls:aclentry_list",
                        name="ACL Entries",
                        permissions=[
                            "nautobot_ip_acls.view_aclentry"
                        ],
                    ),
                ),
            ),
        ),
    ),
    NavMenuTab(
        name="IPAM",
        groups=(
            NavMenuGroup(
                name="IP ACLs",
                weight=250,
                items=(
                    NavMenuItem(
                        link="ipam:ipaddress_list",
                        name="Standard IP ACLs",
                        permissions=["ipam:view_ipaddress"],
                        buttons=(),
                    ),
                ),
            ),
        ),
    ),
    NavMenuTab(
        name="Devices",
        groups=(
            NavMenuGroup(
                name="Devices",
                items=(
                    NavMenuItem(
                        link="plugins:nautobot_ip_acls:device_list",
                        name="IP ACL Audit",
                        permissions=["dcim.view_device"],
                    ),
                ),
            ),
        ),
    ),
)
