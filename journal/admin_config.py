from django.contrib.admin.apps import AdminConfig

class LiteralAdminConfig(AdminConfig):
    default_site = 'journal.admin_dashboard.LiteralAdminSite'
