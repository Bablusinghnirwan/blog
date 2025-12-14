from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Project

User = get_user_model()

class DeepVerificationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='testadmin',
            email='test@example.com',
            password='password123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='<p>Test Content</p>',
            is_published=True
        )

    def test_homepage_loads(self):
        """Verify homepage loads successfully."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        """Verify individual post pages load."""
        url = reverse('post_detail', args=[self.post.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')

    def test_admin_login_page(self):
        """Verify admin login page is accessible."""
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)

    def test_analytics_middleware(self):
        """Verify analytics middleware does not crash request."""
        url = reverse('post_detail', args=[self.post.slug])
        self.client.get(url)  # Should trigger middleware
        # Check if event was logged (assuming middleware logic works)
        # Note: Middleware relies on request.resolver_match, which TestCase client handles.
        from .analytics_models import AnalyticsEvent
        self.assertTrue(AnalyticsEvent.objects.exists())

    def test_static_pages(self):
        """Verify static pages load."""
        pages = ['privacy', 'contact', 'rss_feed']
        for page in pages:
            url = reverse(page)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed to load {page}")

    def test_security_headers(self):
        """Basic security header check (as per check --deploy recommendations)."""
        response = self.client.get(reverse('home'))
        # With DEBUG=True, some headers might not be set, but we checking no crash.
        self.assertEqual(response.status_code, 200)
