from rest_framework import serializers
from .models import Menu, PageComponent

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model. It includes nested children.
    """
    # Using a serializer method field to handle recursion for children
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'url', 'order', 'parent', 'children']

    def get_children(self, obj):
        # Recursively serialize children
        children = obj.children.all()
        serializer = MenuSerializer(children, many=True, context=self.context)
        return serializer.data

class PageComponentSerializer(serializers.ModelSerializer):
    """
    Serializer for the PageComponent model.
    """
    class Meta:
        model = PageComponent
        fields = ['id', 'title', 'content', 'slug']
