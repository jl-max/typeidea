from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    fields = ("title", "abstract", "owner", "tag")
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [
        PostInline,
    ]
    list_display = ("name", "status", "is_nav", "created_time", "post_count")
    fields = ("name", "status", "is_nav")

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "count of posts"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    exclude = ("owner",)
    fields = ("name", "status")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "category"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        "title",
        "category__name",
        "status",
        "created_time",
        "operator",
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ["title", "category__name"]

    actions_on_top = True
    save_on_top = True

    fieldsets = (
        (
            "basic config",
            {
                "description": "basic configration description",
                "fields": (("title", "category"), "status"),
            },
        ),
        (
            "content",
            {
                "fields": ("abstract", "content"),
            },
        ),
        (
            "extra info",
            {
                "classes": ("collapse",),
                "fields": ("tag",),
            },
        ),
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">edit</a>',
            reverse("cus_admin:blog_post_change", args=(obj.id,)),
        )

    operator.short_description = "operation"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
