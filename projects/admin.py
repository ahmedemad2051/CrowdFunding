from django.contrib import admin
from projects.models import Category, Project, Image, Tag


# Register your models here.


class ProjectImageInline(admin.TabularInline):
    model = Image
    extra = 1


class PropertyAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline, ]


admin.site.register(Project, PropertyAdmin)
admin.site.register(Category)
admin.site.register(Tag)
