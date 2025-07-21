from django.db import models
from blog.models import Post


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "normal"),
        (STATUS_DELETE, "delete"),
    )

    target = models.CharField(max_length=100, verbose_name="target")
    content = models.CharField(max_length=2000, verbose_name="content")
    nickname = models.CharField(max_length=50, verbose_name="nickname")
    website = models.URLField(verbose_name="website")
    email = models.EmailField(verbose_name="email")
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="status"
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    def __str__(self):
        return f"comment {self.id}"

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)

    class Meta:
        verbose_name = verbose_name_plural = "comment"
