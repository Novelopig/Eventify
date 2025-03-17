from django.contrib import admin
from .models import Category, Event, Comment, FavoriteEvent, Like, Flag, Attendance

admin.site.site_header = "Eventify - Admin panel"

admin.site.register(Category)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "text", "created_at")
    search_fields = ("user__username", "event__title", "text")
    list_filter = ("created_at", "event", "user")
    ordering = ("-created_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "start_datetime", "end_datetime")
    list_filter = ("title", "category", "description", "created_by")
    search_fields = ("title", "created_by__username", "category__name")


@admin.register(FavoriteEvent)
class FavoriteEventAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "event_category", "event_created_by")
    search_fields = (
        "user__username",
        "event__title",
        "event__category__name",
        "event__created_by__username",
    )
    list_filter = ("event", "user", "event__category", "event__created_by")
    ordering = ("-event__start_datetime",)

    def event_category(self, obj):
        return obj.event.category.name if obj.event.category else "No Category"

    event_category.short_description = "Event Category"

    def event_created_by(self, obj):
        return obj.event.created_by.username

    event_created_by.short_description = "Created By"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "event_category", "event_created_by", "liked_on")
    search_fields = (
        "user__username",
        "event__title",
        "event__category__name",
        "event__created_by__username",
    )
    list_filter = ("event", "user", "event__category", "event__created_by")

    def event_category(self, obj):
        return obj.event.category.name if obj.event.category else "No Category"

    event_category.short_description = "Event Category"

    def event_created_by(self, obj):
        return obj.event.created_by.username

    event_created_by.short_description = "Created By"

    def liked_on(self, obj):
        return obj.event.start_datetime

    liked_on.short_description = "Liked On"


@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "reason", "created_at")
    search_fields = ("user__username", "event__title", "reason")
    list_filter = ("reason", "created_at")
    actions = ["approve_flagged_event", "remove_flagged_event"]

    def approve_flagged_event(self, request, queryset):
        """Approve the flagged event by updating its status."""
        for flag in queryset:
            flag.event.is_approved = True
            flag.event.is_flagged = False
            flag.event.save()
        count = queryset.count()
        self.message_user(request, f"{count} flagged events have been approved.")
        queryset.delete()

    approve_flagged_event.short_description = "Approve flagged events"

    def remove_flagged_event(self, request, queryset):
        """Remove flagged events from the database."""
        count = queryset.count()
        for flag in queryset:
            flag.event.delete()
        queryset.delete()
        self.message_user(request, f"{count} flagged events have been removed.")

    remove_flagged_event.short_description = "Remove flagged events"


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event",
        "event_category",
        "event_created_by",
        "created_at",
        "event_start_datetime",
        "event_end_datetime",
        "event_city",
        "event_province",
    )

    search_fields = ("user__username", "event__title")
    list_filter = ("created_at", "event__category", "event__province", "event__city")

    def event_created_by(self, obj):
        return obj.event.created_by.username if obj.event.created_by else "-"

    event_created_by.short_description = "Created By"

    def event_start_datetime(self, obj):
        return obj.event.start_datetime

    event_start_datetime.short_description = "Start Datetime"

    def event_end_datetime(self, obj):
        return obj.event.end_datetime

    event_end_datetime.short_description = "End Datetime"

    def event_province(self, obj):
        return obj.event.province if obj.event.province else "-"

    event_province.short_description = "Province"

    def event_city(self, obj):
        return obj.event.city if obj.event.city else "-"

    event_city.short_description = "City"

    def event_category(self, obj):
        return obj.event.category.name if obj.event.category else "-"

    event_category.short_description = "Category"
