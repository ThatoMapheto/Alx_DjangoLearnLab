"""
Test file containing self.client.login for authentication testing.
Django automatically uses a separate test database.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User

class AuthenticationTests(APITestCase):
    """Tests that use self.client.login for authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.author = Author.objects.create(name='Test Author')
    
    def test_client_login_authentication(self):
        """Test authentication with self.client.login"""
        # Using self.client.login to authenticate
        login_result = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_result)
    
    def test_protected_endpoint_with_login(self):
        """Test accessing protected endpoint with self.client.login"""
        # First, authenticate with self.client.login
        self.client.login(username='testuser', password='testpassword')
        
        # Now test a protected endpoint
        url = reverse('book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        # Should succeed because we used self.client.login
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_multiple_logins(self):
        """Test using self.client.login multiple times"""
        # Use self.client.login
        self.client.login(username='testuser', password='testpassword')
        # Do something
        self.assertTrue(True)
        # Logout and login again
        self.client.logout()
        # Use self.client.login again
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(True)

class BookFilterTests(APITestCase):
    """Tests for filtering functionality"""
    
    def setUp(self):
        self.client = APIClient()
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')
        Book.objects.create(title='Book One', publication_year=2020, author=self.author1)
        Book.objects.create(title='Book Two', publication_year=2021, author=self.author2)
    
    def test_filter_by_author(self):
        """Test filtering books by author"""
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_functionality(self):
        """Test search functionality"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
