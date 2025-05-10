from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import CVViewSet, upload_cv

router = DefaultRouter()
router.register(r'cvs', CVViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # This will handle /api/cvs/ endpoints
    path('api/', include('chatbot.urls')),  # This will handle /api/chat/ endpoint
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

