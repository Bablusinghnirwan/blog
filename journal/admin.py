from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'view_count', 'is_published', 'published_at', 'updated_at')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'cover_image')
        }),
        ('Media', {
            'fields': ('video_url', 'video_file', 'document'),
            'classes': ('collapse',),
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at', 'view_count', 'created_at', 'updated_at'),
        }),
    )

from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_published', 'sort_order')
    list_filter = ('status', 'is_published')
    search_fields = ('name', 'description', 'tech_stack')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('sort_order', 'status')

from .models import About

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('headline', 'job_current')
    
    def has_add_permission(self, request):
        # Singleton logic: Only allow add if no instance exists
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
