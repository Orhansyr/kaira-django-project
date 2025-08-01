from django.db import models

class Menu(models.Model):
    """
    Represents a menu item in the navigation bar.
    """
    name = models.CharField(max_length=50, help_text="The display name of the menu item.")
    url = models.CharField(max_length=200, help_text="The URL this menu item points to.")
    order = models.IntegerField(default=0, help_text="The order in which the item appears in the menu.")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="The parent menu item, if this is a sub-menu."
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class PageComponent(models.Model):
    """
    Represents a dynamic component on a page that can be edited from the admin panel.
    """
    title = models.CharField(max_length=200, help_text="The title of the component.")
    content = models.TextField(help_text="The main content of the component, can be HTML.")
    slug = models.CharField(
        max_length=100,
        unique=True,
        help_text="A unique identifier for this component, used to load it in the frontend."
    )

    def __str__(self):
        return self.title
