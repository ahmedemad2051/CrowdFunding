from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from users.models import Account
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    desc = models.TextField(max_length=1500)
    owner = models.ForeignKey(to="users.Account", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)
    tags = TaggableManager()
    ratings = GenericRelation(Rating, related_query_name='projects')
    total = models.DecimalField(decimal_places=2, max_digits=10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=False)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.title


def get_image_category_filename(instance, filename):
    slug = instance.name
    # slug = slugify(title)
    return "categories/images/%s-%s" % (slug, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_image_category_filename, null=True)

    def __str__(self):
        return self.name


def get_image_filename(instance, filename):
    slug = instance.project.slug
    # slug = slugify(title)
    return "projects/images/%s-%s" % (slug, filename)


class Image(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.image.__str__()


class Donation(models.Model):
    project = models.ForeignKey(Project, related_name='donations', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project} - {self.amount}"


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    user = models.ForeignKey(to="users.Account", on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)


class Report(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE, related_name='reports')
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey('users.Account', on_delete=models.CASCADE, related_name='reports')
    content = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def report_for(self):
        return self.project or self.comment

    @report_for.setter
    def report_for(self, obj):
        if type(obj) == Project:
            self.project = obj
            self.comment = None
        elif type(obj) == Comment:
            self.comment = obj
            self.project = None
        else:
            raise ValueError("obj parameter must be an object of Project or Comment class")

    def __str__(self):
        return f'{self.user} - {self.report_for}'
