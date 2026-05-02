from django.conf import settings
from django.urls import NoReverseMatch, reverse


# Routes that should emit <link rel="canonical"> because they are public/indexable.
# Keeping this list explicit avoids adding canonicals to utility/account/cart flows.
CANONICAL_ROUTE_NAMES = {
    "index",
    "shop",
    "filtering",
    "contactus",
    "blog",
    "video",
    "single_blog_post",
    "single_product_by_slug",
    "single_product",
}


def _get_canonical_url(request):
    """
    Build the preferred absolute canonical URL for known indexable routes.

    Purpose:
    - Centralize canonical URL generation in one predictable place.
    - Limit canonical tags to explicitly approved public pages only.
    - Always return an absolute URL when a canonical should be emitted.
    """
    resolver_match = getattr(request, "resolver_match", None)
    if not resolver_match or resolver_match.url_name not in CANONICAL_ROUTE_NAMES:
        return None

    url_name = resolver_match.url_name

    # Product pages should always canonicalize to the slug route,
    # even when a legacy name-based URL is used.
    if url_name in {"single_product", "single_product_by_slug"}:
        slug = resolver_match.kwargs.get("slug")
        if slug:
            path = reverse("single_product_by_slug", kwargs={"slug": slug})
            return request.build_absolute_uri(path)
        return None

    try:
        path = reverse(url_name, kwargs=resolver_match.kwargs)
    except NoReverseMatch:
        return None

    return request.build_absolute_uri(path)


def analytics_context(request):
    return {
        # Only enable third-party tracking scripts outside of debug/local mode.
        "TRACKING_ENABLED": not settings.DEBUG,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
        "GOOGLE_SITE_VERIFICATION": settings.GOOGLE_SITE_VERIFICATION,
        # Meta Pixel id for template usage.
        "META_PIXEL_ID": settings.META_PIXEL_ID,
        "canonical_url": _get_canonical_url(request),
    }
