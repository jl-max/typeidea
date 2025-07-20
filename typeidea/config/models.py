from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "normal"),
        (STATUS_DELETE, "delete"),
    )

    title = models.CharField(max_length=50, verbose_name="title")
    href = models.URLField(verbose_name="link")
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="status"
    )
    weight = models.PositiveIntegerField(
        default=1,
        choices=zip(range(1, 6), range(1, 6)),
        verbose_name="weight",
        help_text="Arranged in descending order of weight",
    )
    owner = models.ForeignKey(User, verbose_name="author", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    def __str__(self):
        return f"friendLink {self.id}"

    class Meta:
        verbose_name = verbose_name_plural = "friendLink"


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, "display"),
        (STATUS_HIDE, "hide"),
    )
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, "HTML"),
        (DISPLAY_LATEST, "Newest Articles"),
        (DISPLAY_HOT, "Hottest Articles"),
        (DISPLAY_COMMENT, "Newest Comments"),
    )

    title = models.CharField(max_length=50, verbose_name="title")
    display_type = models.PositiveIntegerField(
        default=1, choices=SIDE_TYPE, verbose_name="display type"
    )
    content = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="content",
        help_text="if not HTML, can be null",
    )
    status = models.PositiveIntegerField(
        default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name="status"
    )
    owner = models.ForeignKey(User, verbose_name="author", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    def __str__(self):
        return f"sideBar {self.id}"

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        from blog.models import Post
        from comment.models import Comment

        result = ""
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {"posts": Post.latest_posts()}
            result = render_to_string("config/blocks/sidebar_posts.html", context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {"posts": Post.hot_posts()}
            result = render_to_string("config/blocks/sidebar_posts.html", context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {"comments": Comment.objects.filter(status=Comment.STATUS_NORMAL)}
            result = render_to_string("config/blocks/sidebar_comments.html", context)
        return result

    class Meta:
        verbose_name = verbose_name_plural = "sideBar"
