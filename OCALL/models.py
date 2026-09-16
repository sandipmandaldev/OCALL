from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.user.username
class Call(models.Model):
    CALL_TYPE_CHOICES = [
        ("audio", "Audio"),
        ("video", "Video"),
    ]
    STATUS_CHOICES = [
        ("calling", "Calling"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("missed", "Missed"),
        ("ended", "Ended"),
    ]
    caller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="outgoing_calls"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="incoming_calls"
    )
    call_type = models.CharField(
        max_length=10,
        choices=CALL_TYPE_CHOICES
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="calling"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.caller.username} → {self.receiver.username}"
class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        ordering = ["timestamp"]
    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"