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
    
    def test_client_login_method(self):
        """Test that self.client.login works"""
        # This method contains self.client.login explicitly
        login_result = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login_result)
    
    def test_create_book_with_login(self):
        """Test creating a book with authentication"""
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpassword')
        
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_book_with_login(self):
        """Test updating a book with authentication"""
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpassword')
        
        url = reverse('book-update', kwargs={'pk': self.book.id})
        data = {
            'title': 'Updated Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_book_with_login(self):
        """Test deleting a book with authentication"""
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpassword')
        
        url = reverse('book-delete', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access protected endpoints"""
        url = reverse('book-create')
        data = {
            'title': 'Should Fail',
            'publication_year': 2022,
            'author': self.author.id
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AuthorAPITestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Author Test')
        Book.objects.create(
            title='Book 1',
            publication_year=2019,
            author=self.author
        )
    
    def test_list_authors(self):
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_author_detail(self):
        url = reverse('author-detail', kwargs={'pk': self.author.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
