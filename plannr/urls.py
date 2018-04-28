from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url('admin/', admin.site.urls),
    url('api/', include('api.urls'))
]
