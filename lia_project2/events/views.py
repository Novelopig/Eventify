from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Event, Category, FavoriteEvent, Like, Flag, Attendance, Comment
from django.conf import settings
from django.utils.timezone import now, timedelta
from django.core.paginator import Paginator


PROVINCES = {
    "ON": ["Toronto", "Ottawa", "Mississauga", "Hamilton"],
    "QC": ["Montreal", "Quebec City", "Laval", "Gatineau"],
}


def get_filtered_events(request):
    query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()
    province = request.GET.get("province", "").strip().upper()
    city = request.GET.get("city", "").strip().title()
    date_filter = request.GET.get("date", "any").strip()

    events = Event.objects.filter(end_datetime__gte=now()).order_by("start_datetime")

    if query:
        events = events.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if selected_category:
        events = events.filter(category__name=selected_category)

    today = now().date()
    if date_filter == "this_week":
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        events = events.filter(start_datetime__date__range=[start_of_week, end_of_week])

    elif date_filter == "next_week":
        start_of_next_week = today + timedelta(days=7 - today.weekday())
        end_of_next_week = start_of_next_week + timedelta(days=6)
        events = events.filter(
            start_datetime__date__range=[start_of_next_week, end_of_next_week]
        )

    if province:
        events = events.filter(province=province)
    if city and city in PROVINCES.get(province, []):
        events = events.filter(city__iexact=city)

    return events


def get_featured_events():
    return Event.objects.annotate(like_count=Count("likes")).order_by("-like_count")[:6]


def homepage(request):
    all_events = get_filtered_events(request).order_by("start_datetime")
    featured_events = all_events.annotate(like_count=Count("likes")).order_by(
        "-like_count"
    )[:6]
    all_events = all_events[:6]
    categories = Category.objects.all()

    user_liked_events = (
        Like.objects.filter(user=request.user).values_list("event_id", flat=True)
        if request.user.is_authenticated
        else []
    )

    return render(
        request,
        "events/homepage.html",
        {
            "featured_events": featured_events,
            "all_events": all_events,
            "query": request.GET.get("q", "").strip(),
            "selected_province": request.GET.get("province", ""),
            "selected_city": request.GET.get("city", ""),
            "categories": categories,
            "provinces": PROVINCES,
            "cities": PROVINCES.get(request.GET.get("province", ""), []),
            "user_liked_events": list(user_liked_events),
        },
    )


@login_required
def toggle_like(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, event=event)

    if created:
        event.likes.add(user)
    else:
        like.delete()
        event.likes.remove(user)

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def toggle_favorite(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    favorite_event, created = FavoriteEvent.objects.get_or_create(
        user=user, event=event
    )

    if not created:
        favorite_event.delete()

    return redirect(request.META.get("HTTP_REFERER", request.path))


@login_required
def toggle_flag(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    existing_flag = Flag.objects.filter(user=user, event=event)

    if existing_flag.exists():
        existing_flag.delete()
    else:
        Flag.objects.create(user=user, event=event, reason="No reason provided")

    return redirect(request.META.get("HTTP_REFERER", "/"))


def event_list(request):
    all_events = get_filtered_events(request)
    categories = Category.objects.all()

    user_liked_events = (
        Like.objects.filter(user=request.user).values_list("event_id", flat=True)
        if request.user.is_authenticated
        else []
    )

    paginator = Paginator(all_events, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "events/event_list.html",
        {
            "page_obj": page_obj,
            "all_events": all_events,
            "selected_province": request.GET.get("province", ""),
            "selected_city": request.GET.get("city", ""),
            "categories": categories,
            "selected_category": request.GET.get("category", "").strip(),
            "selected_date": request.GET.get("date", "any").strip(),
            "provinces": PROVINCES,
            "cities": PROVINCES.get(request.GET.get("province", ""), []),
            "user_liked_events": list(user_liked_events),
        },
    )


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    filtered_events = get_filtered_events(request)

    is_flagged = False
    if request.user.is_authenticated:
        is_flagged = Flag.objects.filter(user=request.user, event=event).exists()

    favorite_events = (
        FavoriteEvent.objects.filter(user=request.user).values_list(
            "event_id", flat=True
        )
        if request.user.is_authenticated
        else []
    )

    comments = Comment.objects.filter(event=event).order_by("-created_at")

    if request.method == "POST":
        if request.user.is_authenticated:
            text = request.POST.get("text").strip()
            if text:
                Comment.objects.create(user=request.user, event=event, text=text)
                return redirect("event_detail", event_id=event.id)
        else:
            return redirect("accounts:login")

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "is_flagged": is_flagged,
            "favorite_events": favorite_events,
            "max_attendees": event.max_attendees,
            "comments": comments,
            "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
            "filtered_events": filtered_events,
            "provinces": PROVINCES,
            "selected_province": request.GET.get("province", "").strip().upper(),
            "selected_city": request.GET.get("city", "").strip().title(),
            "cities": PROVINCES.get(request.GET.get("province", ""), []),
        },
    )


@login_required
def event_creation(request):
    categories = Category.objects.all()
    event = None
    event_id = request.GET.get("edit")
    error_messages = []

    if event_id:
        event = get_object_or_404(Event, id=event_id, created_by=request.user)
        selected_province = event.province
        selected_city = event.city
    else:
        selected_province = request.GET.get("province", "")
        selected_city = request.GET.get("city", "")

    selected_cities = PROVINCES.get(selected_province, [])

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "").strip()
        start_datetime = request.POST.get("start_datetime")
        end_datetime = request.POST.get("end_datetime")
        max_attendees = request.POST.get("max_attendees")
        location = request.POST.get("location")
        province = request.POST.get("province").upper()
        city = request.POST.get("city").title()
        latitude = request.POST.get("latitude") or None
        longitude = request.POST.get("longitude") or None
        category_name = request.POST.get("category")
        image = request.FILES.get("image")

        if province not in PROVINCES.keys():
            error_messages.append(
                f"❌ Invalid Province: '{province}'. Please select a valid province."
            )

        if city and city not in PROVINCES.get(province, []):
            error_messages.append(
                f"❌ Invalid City: '{city}' does not belong to {province}."
            )

        if error_messages:
            return render(
                request,
                "events/event_creation.html",
                {
                    "error_messages": error_messages,
                    "categories": categories,
                    "event": event,
                    "provinces": PROVINCES,
                    "selected_province": province,
                    "selected_city": city,
                    "cities": PROVINCES.get(province, []),
                },
            )

        category = Category.objects.filter(name=category_name).first()
        if not category:
            return render(
                request,
                "events/event_creation.html",
                {
                    "error_messages": ["❌ Invalid category selection."],
                    "categories": categories,
                },
            )

        if event:
            event.title = title
            event.description = description
            event.start_datetime = start_datetime
            event.end_datetime = end_datetime
            event.max_attendees = max_attendees
            event.location = location
            event.province = province
            event.city = city
            event.latitude = latitude
            event.longitude = longitude
            event.category = category
            if image:
                event.image = image
            event.save()

            return redirect("event_detail", event_id=event.id)
        else:
            new_event = Event.objects.create(
                title=title,
                description=description,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                max_attendees=max_attendees,
                location=location,
                province=province,
                city=city,
                latitude=latitude,
                longitude=longitude,
                category=category,
                image=image,
                created_by=request.user,
            )

            return redirect("event_detail", event_id=new_event.id)

    return render(
        request,
        "events/event_creation.html",
        {
            "categories": categories,
            "event": event,
            "provinces": PROVINCES,
            "selected_province": selected_province,
            "selected_city": selected_city,
            "cities": selected_cities,
        },
    )


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == "POST":
        event.delete()
        return redirect("created_events")


@login_required
def toggle_attendance(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    existing_attendance = Attendance.objects.filter(user=user, event=event)
    if existing_attendance.exists():
        existing_attendance.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))

    if event.attendee_count() < event.max_attendees:
        Attendance.objects.create(user=user, event=event)
    else:
        return render(
            request,
            "events/event_detail.html",
            {
                "event": event,
                "error_message": "This event is fully booked.",
            },
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def created_events(request):
    events = Event.objects.filter(created_by=request.user)
    return render(request, "events/my_events.html", {"created_events": events})


@login_required
def favorited_events(request):
    favorited_events = Event.objects.filter(favoriteevent__user=request.user)
    return render(
        request, "events/favorited_events.html", {"favorited_events": favorited_events}
    )


@login_required
def attended_events(request):
    attended_events = Attendance.objects.filter(user=request.user)
    return render(
        request, "events/attended_events.html", {"attended_events": attended_events}
    )
