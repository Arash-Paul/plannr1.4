from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'api'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^login/', views.UserFormLogin.as_view(), name='login'),
    url(r'^users/', views.UserList.as_view(), name='usersdb'),
    url(r'^register/', views.Register.as_view(), name='register'),
    # url(r'^signup/', views.UserFormSignup.as_view(), name='signup'),
    url(r'^eventform/', views.EventCreationForm.as_view(), name='eventform'),
    url(r'^createdeventslist/', views.CreatedEventList.as_view(), name='owneventslist'),
    url(r'^logout/$', views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
