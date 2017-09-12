import uuid

# from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models


class Blogpost(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    title = models.CharField(max_length=256)    # Unique title constraint not implemented
    content = JSONField(null=True)   # Max size of JSON is 1 GB
    created_at = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    blog = models.ForeignKey(Blogpost)
    para = models.IntegerField(default=0)   # A default value 0 would be comment on blog and not para
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
