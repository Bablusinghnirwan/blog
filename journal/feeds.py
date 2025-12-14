from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "Literal. Writing"
    link = "/writing/"
    description = "Notes on work, learning, and thinking."

    def items(self):
        return Post.objects.filter(is_published=True).order_by('-published_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        import re
        clean_text = re.sub('<[^<]+?>', '', item.content)
        return clean_text[:200] + '...'

    def item_link(self, item):
        return reverse('post_detail', args=[item.slug])
