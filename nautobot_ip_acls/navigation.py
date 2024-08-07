"""Module to change nautobot navigation menu."""

from nautobot.apps.ui import NavMenuGroup, NavMenuItem, NavMenuTab

menu_items = (
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
)
