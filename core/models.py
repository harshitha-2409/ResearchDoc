from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Resource(models.Model):

    RESOURCE_TYPES = [
        ('PDF', 'PDF'),
        ('LINK', 'External Link'),
        ('DOC', 'Document'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='resources'
    )

    title = models.CharField(max_length=200)

    resource_type = models.CharField(
        max_length=10,
        choices=RESOURCE_TYPES
    )

    file = models.FileField(
        upload_to='resources/',
        blank=True,
        null=True
    )

    external_url = models.URLField(
        blank=True,
        null=True
    )

    authors = models.CharField(
        max_length=255,
        blank=True
    )

    publication_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    abstract_text = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Summary(models.Model):

    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='summaries'
    )

    summary_text = models.TextField()

    citation_text = models.TextField(blank=True)

    key_findings = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.resource.title}"


class Tag(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class ResourceTag(models.Model):

    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('resource', 'tag')


class Comparison(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='comparisons'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ComparisonItem(models.Model):

    comparison = models.ForeignKey(
        Comparison,
        on_delete=models.CASCADE,
        related_name='items'
    )

    item_name = models.CharField(max_length=200)

    criteria = models.TextField()

    notes = models.TextField(blank=True)

    rating = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.item_name