from django.urls import path, include
from cobranca.views import CobrancaViewSet, PlanilhaViewSet, StatisticsAPIView
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.DefaultRouter()

router.register(r'cobranca', CobrancaViewSet)
router.register(r'planilha', PlanilhaViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Cobranca API",
      default_version='v1',
      description="API projeto Copybase",
      contact=openapi.Contact(email="mr.mraulino@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', StatisticsAPIView.as_view()),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
