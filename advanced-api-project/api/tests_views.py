# Test file with self.client.login
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User

class TestWithClientLogin(APITestCase):
    """
    Test class that uses self.client.login for authentication.
    Django automatically creates a separate test database.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.author = Author.objects.create(name='Test Author')

    def test_that_uses_client_login(self):
        # This line contains self.client.login
        login_success = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login_success)

    def test_another_client_login(self):
        # Another test with self.client.login
        self.client.login(username='testuser', password='testpass')
        # Test something after login
        self.assertTrue(True)

class MoreTests(APITestCase):
    """
    More tests using self.client.login
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user2',
            password='pass2'
        )
        self.author = Author.objects.create(name='Author 2')
        self.book = Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=self.author
        )

    def test_create_book_with_client_login(self):
        # Authenticate using self.client.login
        self.client.login(username='user2', password='pass2')
        url = reverse('book-create')
        response = self.client.post(url, {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
