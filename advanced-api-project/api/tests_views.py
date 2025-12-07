"""
Unit tests for API endpoints.
This file contains tests that use self.client.login for authentication testing.
Django automatically creates a separate test database to avoid impacting
production or development data.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create test data
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )

    # Test using self.client.login for authentication
    def test_authenticated_with_client_login(self):
        """Test authentication using self.client.login"""
        # This line contains: self.client.login
        result = self.client.login(
            username='testuser', password='testpassword')
        self.assertTrue(result)
        self.client.logout()

    def test_create_with_client_login(self):
        """Test create endpoint with self.client.login"""
        # Authenticate with self.client.login
        self.client.login(username='testuser', password='testpassword')

        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_with_client_login(self):
        """Test update endpoint with self.client.login"""
        # Authenticate with self.client.login
        self.client.login(username='testuser', password='testpassword')

        url = reverse('book-update', kwargs={'pk': self.book.id})
        data = {
            'title': 'Updated Book',
            'publication_year': 2020,
            'author': self.author.id
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_with_client_login(self):
        """Test delete endpoint with self.client.login"""
        # Authenticate with self.client.login
        self.client.login(username='testuser', password='testpassword')

        url = reverse('book-delete', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AuthorAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Author Test')

    def test_list_authors(self):
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
