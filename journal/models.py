from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from .analytics_models import AnalyticsEvent # Ensure it's imported for migrations

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    
    # Video support
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or Vimeo URL")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Upload a video file")
    
    # Document support
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    
    view_count = models.PositiveIntegerField(default=0, editable=False)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at', '-created_at']

class Project(models.Model):
    STATUS_CHOICES = (
        ('running', 'Running'),
        ('completed', 'Completed'),
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=255, help_text="One-line description for the index page")
    content = RichTextField(help_text="Detailed project overview")
    tech_stack = models.CharField(max_length=255, help_text="e.g. Django, React, Postgres")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    
    # Optional links
    live_url = models.URLField(blank=True, null=True)
    repo_url = models.URLField(blank=True, null=True)
    
    # Media
    cover_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    
    view_count = models.PositiveIntegerField(default=0, editable=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_order', '-created_at']

class About(models.Model):
    """Singleton model for About page content."""
    headline = models.CharField(max_length=200, default="I am a Product Designer and Full-Stack Engineer.")
    bio = RichTextField(help_text="Main long-form bio content.")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    
    # Section: Connect
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Section: Experience (Simple fields)
    job_current = models.CharField(max_length=100, default="Stripe")
    job_current_role = models.CharField(max_length=100, default="Senior Product Designer")
    job_current_date = models.CharField(max_length=50, default="2020 — Present")
    
    job_previous = models.CharField(max_length=100, default="Vercel", blank=True)
    job_previous_role = models.CharField(max_length=100, default="Frontend Engineer", blank=True)
    job_previous_date = models.CharField(max_length=50, default="2018 — 2020", blank=True)
    
    capabilities = models.CharField(max_length=300, help_text="Comma separated list", default="React, Next.js, Django, PostgreSQL, AWS, Figma, System Design")

    class Meta:
        verbose_name_plural = "About Profile"

    def __str__(self):
        return "About Profile"

    def save(self, *args, **kwargs):
        if not self.pk and About.objects.exists():
            return
        super().save(*args, **kwargs)
