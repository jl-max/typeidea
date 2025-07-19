from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "normal"),
        (STATUS_DELETE, "delete"),
    )

    name = models.CharField(max_length=50, verbose_name="name")
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="status"
    )
    is_nav = models.BooleanField(default=False, verbose_name="is navigation")
    owner = models.ForeignKey(User, verbose_name="author", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {"navs": nav_categories, "categories": normal_categories}

    class Meta:
        verbose_name = verbose_name_plural = "category"


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "normal"),
        (STATUS_DELETE, "delete"),
    )

    name = models.CharField(max_length=50, verbose_name="name")
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="status"
    )
    owner = models.ForeignKey(User, verbose_name="author", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "tag"


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, "normal"),
        (STATUS_DELETE, "delete"),
        (STATUS_DRAFT, "draft"),
    )

    title = models.CharField(max_length=255, verbose_name="title")
    abstract = models.CharField(max_length=1024, blank=True, verbose_name="abstract")
    content = models.TextField(
        verbose_name="content", help_text="content must be markdown format."
    )
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="status"
    )
    category = models.ForeignKey(
        Category, verbose_name="category", on_delete=models.CASCADE
    )
    tag = models.ForeignKey(Tag, verbose_name="tag", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name="author", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related(
                "owner", "category"
            )

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(
                status=Post.STATUS_NORMAL
            ).select_related("owner", "category")

        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    class Meta:
        verbose_name = verbose_name_plural = "article"
        ordering = ["-id"]
