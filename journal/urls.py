from django.urls import path
from .views import HomeView, PostDetailView, ProjectListView, ProjectDetailView, AboutView, WritingListView
from .feeds import LatestPostsFeed
from django.views.generic import TemplateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('writing/', WritingListView.as_view(), name='writing_list'),
    path('writing/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('about/', AboutView.as_view(), name='about'),
    
    # Static Pages
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('rss-info/', TemplateView.as_view(template_name='rss_info.html'), name='rss_info'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    
    # Actual Feed
    path('rss/', LatestPostsFeed(), name='rss_feed'),
]
