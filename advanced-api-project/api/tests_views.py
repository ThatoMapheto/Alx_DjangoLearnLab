from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):
    """
    Test case for Book API endpoints.
    """

    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()

        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')

        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author2
        )

    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can list books"""
        url = reverse('book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book_detail(self):
        """Test retrieving a single book by ID"""
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated(self):
        """Test that authenticated users can create books"""
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create')

        data = {
            'title': 'New Test Book',
            'publication_year': 2020,
            'author': self.author1.id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        url = reverse('book-create')

        data = {
            'title': 'New Test Book',
            'publication_year': 2020,
            'author': self.author1.id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """Test that authenticated users can update books"""
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-update', kwargs={'pk': self.book1.id})

        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books"""
        url = reverse('book-update', kwargs={'pk': self.book1.id})

        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books"""
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-delete', kwargs={'pk': self.book1.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        url = reverse('book-delete', kwargs={'pk': self.book1.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year"""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1949})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_search_books_by_title(self):
        """Test searching books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'],
                         'Harry Potter and the Philosopher\'s Stone')

    def test_search_books_by_author_name(self):
        """Test searching books by author name"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Orwell'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_order_books_by_title(self):
        """Test ordering books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_publication_year_desc(self):
        """Test ordering books by publication year descending"""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        publication_years = [book['publication_year']
                             for book in response.data]
        self.assertEqual(publication_years, sorted(
            publication_years, reverse=True))

    def test_publication_year_validation(self):
        """Test that publication year validation works"""
        # Use self.client.login to authenticate
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create')

        future_year = 2030
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Publication year cannot be in the future',
                      str(response.data))


class AuthorAPITestCase(APITestCase):
    """Test case for Author API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )

    def test_list_authors(self):
        """Test listing all authors"""
        url = reverse('author-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_author_with_books(self):
        """Test retrieving author details with nested books"""
        url = reverse('author-detail', kwargs={'pk': self.author.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'Test Book')
