from django import template
from django.utils.html import format_html

register = template.Library()

STATUS_TONES = {
    "Available": "green", "Completed": "green", "Paid": "green", "Active": "green",
    "Reserved": "amber", "Pending": "amber", "Negotiation": "amber", "Scheduled": "amber",
    "Rented": "blue", "Viewing": "blue", "Contacted": "blue",
    "New": "slate", "Draft": "slate",
    "Sold": "red", "Cancelled": "red",
}


@register.filter
def status_badge(value):
    """Render a status value as a colored pill."""
    if value in (None, ""):
        return ""
    return format_html('<span class="badge-status badge-status--{}">{}</span>', STATUS_TONES.get(str(value), "slate"), value)


@register.filter
def initials(user):
    """Up to two initials for an avatar, from full name or username."""
    name = (user.get_full_name() or user.get_username() or "?").split()
    return "".join(part[0] for part in name[:2]).upper()


@register.simple_tag(takes_context=True)
def nav_active(context, *prefixes):
    """Return 'active' when the current URL name starts with one of the prefixes."""
    match = getattr(context.get("request"), "resolver_match", None)
    name = getattr(match, "url_name", "") or ""
    return "active" if any(name.startswith(prefix) for prefix in prefixes) else ""
