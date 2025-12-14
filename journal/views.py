from django.views.generic import ListView, DetailView
from django.db.models import F
from .models import Post

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

class WritingListView(ListView):
    model = Post
    template_name = 'writing.html'
    context_object_name = 'posts'
    paginate_by = 20 # Show more posts in archive view
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-published_at')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count safely
        Post.objects.filter(pk=obj.pk).update(view_count=F('view_count') + 1)
        obj.refresh_from_db()
        return obj

from django.views.generic import TemplateView
from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True)

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

class AboutView(TemplateView):
    template_name = 'about.html'
