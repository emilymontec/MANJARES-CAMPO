from django.conf import settings


def app_context(request):
    return {
        "WHATSAPP_NUMBER": getattr(settings, "WHATSAPP_NUMBER", ""),
        "BUSINESS_HOURS": getattr(settings, "BUSINESS_HOURS", "Lun-Sáb 8:00-18:00 · Dom 8:00-13:00"),
        "SOCIAL_FACEBOOK_URL": getattr(settings, "SOCIAL_FACEBOOK_URL", "#"),
        "SOCIAL_INSTAGRAM_URL": getattr(settings, "SOCIAL_INSTAGRAM_URL", "#"),
    }
