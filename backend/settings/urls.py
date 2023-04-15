from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from auths.views import (
    MyTokenObtainPairView,
    register_user,
    activate_user,

)
from main.views import (
    GamerViewSet,
    GameObjectViewSet,
)


router = DefaultRouter(
    trailing_slash=False
)
router.register('gamers', GamerViewSet)
router.register('objects', GameObjectViewSet, basename='gameobject')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', MyTokenObtainPairView.as_view()),
    path('api/', include(router.urls)),
    path('api/register', register_user),
    path('api/activate/<str:activation_code>', activate_user),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
