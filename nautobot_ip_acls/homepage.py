"""Module to change nautobot homepage."""

from nautobot.apps.ui import HomePageItem, HomePagePanel
from nautobot.extras.models import Status

layout = (
    HomePagePanel(
        name="Organization",
        items=(
            HomePageItem(
                name="Statuses",
                model=Status,
                weight=300,
                link="extras:status_list",
                description="Customizable object statuses",
                permissions=["extras.view_status"],
            ),
        ),
    ),
)
