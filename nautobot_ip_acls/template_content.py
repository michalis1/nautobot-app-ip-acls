"""Module to change object details view."""

from django.urls import reverse
from nautobot.apps.ui import TemplateExtension


# pylint: disable=W0223
class IPACLDeviceTemplateExtension(TemplateExtension):
    """Add IP ACL information to the Nautobot Device detail view."""

    model = "dcim.device"

    def right_page(self):
        """Add content on the right side of the view."""
        # Get the object that was provided as template context;
        # in this case, the Device object itself.
        device = self.context["object"]
        # Render the config context of this Device as a Python dict:
        config_context_data = device.get_config_context()
        # Get the contents of the "access_lists" key in the dict:
        acls = config_context_data.get("access_lists", {})
        # Construct the HTML to contain this data
        # Start a panel containing an unordered list:
        output = """
            <div class="panel panel-default">
            <div class="panel-heading"><strong>IP ACLs</strong></div>
            <div class="panel-body">
            <ul>
        """
        # Add list entries based on the available data:
        for acl_id, acl_entries in acls.items():
            output += f"<li>ACL <code>{acl_id}</code> " f"with {len(acl_entries)} entries</li>"
        # End the list and the panel
        output += "</ul></div></div>"
        return output

    def detail_tabs(self):
        return [
            {
                "title": "IP ACLs",
                "url": reverse("plugins:nautobot_ip_acls:device_ip_acls", kwargs={"pk": self.context["object"].pk}),
            },
        ]


# pylint: disable=W0223
class StatusContent(TemplateExtension):
    """Status Detail View."""

    model = "extras.status"

    def right_page(self):
        """Content for right page."""
        return """
            <div class="panel panel-default">
                <div class="panel-heading">
                    <strong>Status Information</strong>
                </div>
                <div class="panel-body">
                    Hello!
                </div>
            </div>
        """


template_extensions = [StatusContent, IPACLDeviceTemplateExtension]  # Important to include!
