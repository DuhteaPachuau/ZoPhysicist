from .models import Category


def site_context(request):
    return {
        "site_name": "ZoPhysicist",
        "nav_categories": Category.objects.prefetch_related("lessons").all()[:6],
    }
