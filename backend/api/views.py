from rest_framework import viewsets, permissions
from .models import Menu, PageComponent
from .serializers import MenuSerializer, PageComponentSerializer

class MenuViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows menus to be viewed or edited.
    Returns only top-level menu items, with children nested.
    """
    # We only want to return top-level menu items in the main list view.
    # Children will be nested in the serializer's response.
    queryset = Menu.objects.filter(parent__isnull=True)
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PageComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows page components to be viewed or edited.
    Can be looked up by slug.
    """
    queryset = PageComponent.objects.all()
    serializer_class = PageComponentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug' # Use slug for retrieving components
    # Optional: If you want to allow lookup by pk as well
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     # try to find by slug
    #     try:
    #         obj = queryset.get(slug=self.kwargs[self.lookup_field])
    #     except PageComponent.DoesNotExist:
    #         # if not found, try by pk
    #         obj = super().get_object()
    #     return obj
