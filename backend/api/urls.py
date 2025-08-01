from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, PageComponentViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'components', PageComponentViewSet, basename='pagecomponent')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
