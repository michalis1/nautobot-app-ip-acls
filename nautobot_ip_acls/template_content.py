"""Module to change object details view."""

from nautobot.apps.ui import TemplateExtension


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


template_extensions = [StatusContent]  # Important to include!
