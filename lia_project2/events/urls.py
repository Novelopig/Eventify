from django.urls import path
from . import views
from .views_admin import admin_statistics

from .views import (
    homepage,
    event_list,
    event_detail,
    event_creation,
    toggle_like,
    toggle_favorite,
    toggle_flag,
    toggle_attendance,
    attended_events,
    delete_event,
)

urlpatterns = [
    path("", homepage, name="homepage"),
    path("admin/statistics/", admin_statistics, name="admin_statistics"),
    path("list/", event_list, name="event_list"),
    path("<int:event_id>/", event_detail, name="event_detail"),
    path("event_creation/", event_creation, name="event_creation"),
    path("events/<int:event_id>/delete/", delete_event, name="delete_event"),
    path("events/<int:event_id>/like/", toggle_like, name="toggle_like"),
    path("events/<int:event_id>/favorite/", toggle_favorite, name="toggle_favorite"),
    path("events/<int:event_id>/flag/", toggle_flag, name="toggle_flag"),
    path("events/<int:event_id>/attend/", toggle_attendance, name="toggle_attendance"),
    path("dashboard/favorited-events/", views.favorited_events, name="favorite-events"),
    path("dashboard/attended-events/", attended_events, name="attended-events"),
    path("my-events/", views.created_events, name="created_events"),
    path("event/<int:event_id>/", event_detail, name="event-detail"),
]
