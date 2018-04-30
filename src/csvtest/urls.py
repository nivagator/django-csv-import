"""csvtest URL Configuration

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
from django.contrib import admin
from django.urls import path

from fileimport.views import home, simple_upload, download, ImportList, ImportHistoryView

app_name = 'csvtest'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('import/', simple_upload, name='import'),
    path('import/history/', ImportHistoryView.as_view(), name='history'),
    path('import/group/', ImportList.as_view(), name='warehouse'),
    path('import/group/<slug:slug>/', ImportList.as_view(), name='validate'),
    path('download/<path:path>/', download, name='download'),
   
]

# if settings.DEBUG:
#     # static files (images, css, javascript, etc.)
#     urlpatterns += patterns('',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#         'document_root': settings.MEDIA_ROOT}))