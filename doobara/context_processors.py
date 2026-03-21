from django.conf import settings


def analytics_context(request):
    return {
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
        "GOOGLE_SITE_VERIFICATION": settings.GOOGLE_SITE_VERIFICATION,
        # Meta Pixel id for template usage.
        "META_PIXEL_ID": settings.META_PIXEL_ID,
    }
