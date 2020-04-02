from django.db import models


class Activation(models.Model):
    user = models.ForeignKey("users.Account", on_delete=models.CASCADE, related_name='activation')
    token = models.CharField(max_length=50, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'
