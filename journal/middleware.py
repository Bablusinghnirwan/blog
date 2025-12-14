from .analytics_models import AnalyticsEvent
from .models import Post, Project

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Track authenticated admin traffic? Maybe not.
        # Track public traffic only?
        # User said "views visible only to admin", but we track all views usually.
        # Let's simple track GET 200 requests to Detail Views
        
        if response.status_code == 200 and request.method == 'GET' and not request.path.startswith('/admin'):
            user_agent = request.headers.get('User-Agent', '')[:255]
            ip = self.get_client_ip(request)
            
            # Simple heuristic: Look for attributes in the callback (standard Django flow)
            # OR just look at resolver match.
            
            if hasattr(request, 'resolver_match') and request.resolver_match:
                if request.resolver_match.url_name == 'post_detail':
                    # Need to fetch object? View already did. 
                    # But middleware runs after view.
                    # We can assume URL slug logic, or cache object in request.
                    slug = request.resolver_match.kwargs.get('slug')
                    if slug:
                        try:
                            # This is duplicate DB hit but safest middleware approach without touching views deeply
                            post = Post.objects.get(slug=slug)
                            AnalyticsEvent.objects.create(content_object=post, ip_address=ip, user_agent=user_agent)
                        except Post.DoesNotExist:
                            pass
                
                elif request.resolver_match.url_name == 'project_detail':
                    slug = request.resolver_match.kwargs.get('slug')
                    if slug:
                        try:
                            project = Project.objects.get(slug=slug)
                            AnalyticsEvent.objects.create(content_object=project, ip_address=ip, user_agent=user_agent)
                        except Project.DoesNotExist:
                            pass

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
