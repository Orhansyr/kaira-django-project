from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Menu, PageComponent

class PageComponentAPITests(APITestCase):
    def setUp(self):
        """Set up a test user and a sample PageComponent."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.component_data = {'title': 'About Us', 'content': 'This is the about page.', 'slug': 'about-us'}
        self.component = PageComponent.objects.create(**self.component_data)

    def test_list_components_unauthenticated(self):
        """Ensure unauthenticated users can list page components."""
        response = self.client.get('/api/components/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.component_data['title'])

    def test_detail_component_unauthenticated(self):
        """Ensure unauthenticated users can retrieve a single page component by slug."""
        response = self.client.get(f'/api/components/{self.component.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.component_data['title'])

    def test_create_component_unauthenticated(self):
        """Ensure unauthenticated users CANNOT create components."""
        response = self.client.post('/api/components/', {'title': 'New', 'content': 'Content', 'slug': 'new'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_component_authenticated(self):
        """Ensure authenticated users CAN create components."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/components/', {'title': 'New', 'content': 'Content', 'slug': 'new'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PageComponent.objects.count(), 2)

    def test_update_component_authenticated(self):
        """Ensure authenticated users CAN update components."""
        self.client.force_authenticate(user=self.user)
        updated_data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/components/{self.component.slug}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        self.component.refresh_from_db()
        self.assertEqual(self.component.title, 'Updated Title')

class MenuAPITests(APITestCase):
    def setUp(self):
        """Set up a test user and a sample Menu with a child."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.menu1 = Menu.objects.create(name='Home', url='/', order=1)
        self.menu2 = Menu.objects.create(name='About', url='/about', order=2, parent=self.menu1)

    def test_list_menus(self):
        """Ensure the API returns only top-level menu items."""
        response = self.client.get('/api/menus/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return the top-level menu 'Home'
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.menu1.name)

    def test_nested_menus(self):
        """Ensure nested menu items are returned within their parent."""
        response = self.client.get('/api/menus/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['children']), 1)
        self.assertEqual(response.data[0]['children'][0]['name'], self.menu2.name)

    def test_create_menu_authenticated(self):
        """Ensure authenticated users can create menu items."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/menus/', {'name': 'Contact', 'url': '/contact', 'order': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)

    def test_delete_menu_unauthenticated(self):
        """Ensure unauthenticated users CANNOT delete menu items."""
        response = self.client.delete(f'/api/menus/{self.menu1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Menu.objects.filter(id=self.menu1.id).exists())
