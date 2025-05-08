from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, CustomAuthToken, get_user_role,
    ProductViewSet, CheckoutViewSet,
    checkout_view, admin_checkout_list
)

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('checkouts', CheckoutViewSet)

urlpatterns = [
    path('api/register/', RegisterView.as_view()),
    path('api/login/', CustomAuthToken.as_view()),
    path('api/role/', get_user_role),
    path('api/checkout/', checkout_view, name='checkout'),
    path('api/admin/checkouts/', admin_checkout_list, name='admin-checkout-list'),  # Note trailing slash
    path('api/', include(router.urls)),
]
