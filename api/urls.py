from rest_framework.routers import DefaultRouter
from .views import Users

router = DefaultRouter()
router.register(r'user', Users)

urlpatterns = router.urls