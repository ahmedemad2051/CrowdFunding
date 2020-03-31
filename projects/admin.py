from django.contrib import admin
from projects.models import Category, Project, Image, Comment, Report


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


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('project', 'comment', 'user', 'content', 'created_at', 'seen')
    list_filter = ('project', 'seen', 'created_at')
    search_fields = ('user', 'project', 'comment')
    actions = ['handle_report']

    def handle_report(self, request, queryset):
        queryset.update(seen=True)


admin.site.register(Project, PropertyAdmin)
admin.site.register(Category)
