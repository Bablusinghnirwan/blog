from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Post, Project
from .analytics_models import AnalyticsEvent

# Customizing the default AdminSite.index
class LiteralAdminSite(admin.AdminSite):
    site_header = "Literal Studio"
    site_title = "Literal"
    index_title = "Studio Dashboard"

    def index(self, request, extra_context=None):
        # Stats
        post_count = Post.objects.filter(is_published=True).count()
        project_count = Project.objects.filter(is_published=True).count()
        
        # Total views (from simple generic count + analytics events logic if needed)
        # For now, let's just sum the view_count field
        post_views = Post.objects.aggregate(Sum('view_count'))['view_count__sum'] or 0
        project_views = Project.objects.aggregate(Sum('view_count'))['view_count__sum'] or 0
        total_views = post_views + project_views
        
        # Today's views (from AnalyticsEvent)
        today = timezone.now().date()
        todays_views = AnalyticsEvent.objects.filter(timestamp__date=today).count()
        
        # Top Content
        top_posts = Post.objects.filter(is_published=True).order_by('-view_count')[:5]
        top_content = []
        for p in top_posts:
            top_content.append({'title': p.title, 'type': 'Post', 'view_count': p.view_count})
            
        extra_context = extra_context or {}
        extra_context.update({
            'post_count': post_count,
            'project_count': project_count,
            'total_views': total_views,
            'todays_views': todays_views,
            'top_content': top_content,
        })
        return super().index(request, extra_context=extra_context)

# We can't easily swap the AdminSite instance without changing urls.py
# Alternatively, we can patch the default site or just update urls.py to use this one.
# For simplicity in this flow, we will just patch the index context via index_template override 
# OR use a simpler approach: Patch the `admin.site.index` view logic isn't easy.
# Better approach: Create a custom view for the dashboard and direct the "Home" link in Jazzmin to it?
# Or: Overwrite `admin.site.index` method.
