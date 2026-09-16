from django.contrib import admin
from .models import Profile, Call, Message

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "is_online", "last_seen")
    list_filter = ("is_online",)
    search_fields = ("user__username", "user__email", "phone")
@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = (
        "caller",
        "receiver",
        "call_type",
        "status",
        "started_at",
        "answered_at",
        "ended_at",
        "duration",
    )
    list_filter = ("call_type", "status")
    search_fields = (
        "caller__username",
        "receiver__username",
    )
    readonly_fields = (
        "started_at",
        "answered_at",
        "ended_at",
    )
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "receiver",
        "message",
        "timestamp",
        "is_read",
    )
    list_filter = ("is_read",)
    search_fields = (
        "sender__username",
        "receiver__username",
        "message",
    )
    readonly_fields = ("timestamp",)