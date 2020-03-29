from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    desc = models.TextField()
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)
    tags = models.ManyToManyField(to="Tag")
    total = models.DecimalField(decimal_places=2, max_digits=10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

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


class Tag(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
