"""DCStats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.i18n import JavaScriptCatalog
import home.views
import stats.views
import chiefs.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home.views.home, name="home"),
    path("chiefs/pilot_log", chiefs.views.chiefs_log, name="chiefs_log"),
    path("chiefs/log_entry", chiefs.views.chiefs_log_entry, name="chiefs_log_entry"),
    path("chiefs/new_log", chiefs.views.new_log, name="chiefs_new_log"),
    path("stats/log_entry", stats.views.log_entry, name="logstats"),
    path("stats/pilot_stats", stats.views.pilot_stats, name="pilot_stats"),
    path("stats/pilot_log", stats.views.pilot_log, name="pilot_log"),
    path("stats/new_log", stats.views.new_log, name="new_log"),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    re_path(r"^accounts/inactive", home.views.inactive, name="inactive"),
    path("accounts/signup", home.views.signup, name="signup"),
    path(
        "accounts/login",
        auth_views.LoginView.as_view(template_name="home/login.html"),
        name="login",
    ),
    path(
        "accounts/logout",
        auth_views.LogoutView.as_view(template_name="home/logout.html"),
        name="logout",
    ),
    path("accounts/profile", home.views.profile, name="profile"),
    path("accounts/unauthorized", home.views.unauthorized, name="unauthorized"),
    path("privacy", stats.views.privacy, name="privacy"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
