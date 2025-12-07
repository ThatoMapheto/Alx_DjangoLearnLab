"""
Test file containing self.client.login for authentication testing
and response.data for checking response content.
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
        self.book = Book.objects.create(
            title='Existing Book',
            publication_year=2020,
            author=self.author
        )
    
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
        # Check response.data
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_book_list_response_data(self):
        """Test that book list returns correct response.data"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data structure
        self.assertIsInstance(response.data, list)
        # Check content in response.data
        if len(response.data) > 0:
            self.assertIn('title', response.data[0])
    
    def test_book_detail_response_data(self):
        """Test that book detail returns correct response.data"""
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data content
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'], 'Existing Book')
        self.assertIn('publication_year', response.data)
        self.assertEqual(response.data['publication_year'], 2020)
    
    def test_update_book_with_login_and_response_data(self):
        """Test updating book with login and checking response.data"""
        # Authenticate with self.client.login
        self.client.login(username='testuser', password='testpassword')
        
        url = reverse('book-update', kwargs={'pk': self.book.id})
        data = {
            'title': 'Updated Book Title',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'], 'Updated Book Title')
    
    def test_filter_books_response_data(self):
        """Test filtering books and checking response.data"""
        # Create another book
        Book.objects.create(
            title='Another Book',
            publication_year=2022,
            author=self.author
        )
        
        url = reverse('book-list')
        # Test without filter
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data length
        self.assertEqual(len(response.data), 2)
        
        # Test with filter
        response = self.client.get(url, {'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            self.assertIn('title', book)
    
    def test_search_books_response_data(self):
        """Test searching books and checking response.data"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Existing'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data
        self.assertGreater(len(response.data), 0)
        self.assertIn('title', response.data[0])
    
    def test_ordering_books_response_data(self):
        """Test ordering books and checking response.data"""
        # Create another book with different title
        Book.objects.create(
            title='AAA First Book',
            publication_year=2019,
            author=self.author
        )
        
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data is ordered
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

class AuthorTests(APITestCase):
    """Tests for author endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
    
    def test_author_list_response_data(self):
        """Test author list response.data"""
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data
        self.assertIsInstance(response.data, list)
        if len(response.data) > 0:
            author_data = response.data[0]
            self.assertIn('name', author_data)
            self.assertIn('books', author_data)
    
    def test_author_detail_response_data(self):
        """Test author detail response.data"""
        url = reverse('author-detail', kwargs={'pk': self.author.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check response.data
        self.assertIn('name', response.data)
        self.assertIn('books', response.data)
        self.assertEqual(response.data['name'], 'Test Author')
        # Check nested books in response.data
        self.assertIsInstance(response.data['books'], list)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'Test Book')

class UnauthenticatedTests(APITestCase):
    """Tests for unauthenticated access"""
    
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Test Author')
    
    def test_unauthenticated_create_book(self):
        """Test that unauthenticated users cannot create books"""
        url = reverse('book-create')
        data = {
            'title': 'Should Fail',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Check response.data for error message
        self.assertIn('detail', response.data)
