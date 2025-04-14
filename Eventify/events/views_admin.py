# events/views_admin.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from .models import Event
from django.contrib.auth import get_user_model


@staff_member_required
def admin_statistics(request):
    total_events = Event.objects.count()
    total_likes = Event.objects.aggregate(total=Count("likes"))
    total_flagged = Event.objects.filter(flagged_by__isnull=False).distinct().count()
    User = get_user_model()
    total_users = User.objects.count()

    most_commented_events = Event.objects.annotate(
        comment_count=Count("comments")
    ).order_by("-comment_count")[:5]
    most_commented_users = User.objects.annotate(
        comment_count=Count("comment")
    ).order_by("-comment_count")[:5]

    context = {
        "total_events": total_events,
        "total_likes": total_likes.get("total") or 0,
        "total_flagged": total_flagged,
        "total_users": total_users,
        "most_commented_events": most_commented_events,
        "most_commented_users": most_commented_users,
    }
    return render(request, "events/admin/statistics.html", context)
