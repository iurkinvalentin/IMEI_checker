from django.db import models


class AllowedUser(models.Model):
    """Белый список"""
    user_id = models.BigIntegerField(
        unique=True, verbose_name="Telegram ID")
    username = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Username")
    added_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлен")

    def __str__(self):
        return (
            f"{self.username} ({self.user_id})"
            if self.username else str(self.user_id))

    class Meta:
        verbose_name = "Разрешённый пользователь"
        verbose_name_plural = "Разрешённые пользователи"
