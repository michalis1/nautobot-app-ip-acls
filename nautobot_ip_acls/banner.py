"""Module to change nautobot banner."""

from django.utils.html import format_html
from nautobot.apps.ui import Banner, BannerClassChoices


def banner(context, *args, **kwargs):
    """Banner content greeting the user."""
    content = format_html(
        "<div>Hello, <strong>{}</strong>! 👋</div>",
        context.request.user,
    )
    return Banner(content=content, banner_class=BannerClassChoices.CLASS_SUCCESS)
