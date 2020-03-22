from django.db import models


# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE)
    tags = models.ManyToManyField(to="Tag")
    total = models.DecimalField(decimal_places=2, max_digits=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField()


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
