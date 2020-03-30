from django.contrib import admin
from projects.models import Category, Project, Image, Comment


# Register your models here.


class ProjectImageInline(admin.TabularInline):
    model = Image
    extra = 1


class PropertyAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'body', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('user', 'project', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Project, PropertyAdmin)
admin.site.register(Category)
