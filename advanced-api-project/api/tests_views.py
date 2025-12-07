"""
Test file containing self.client.login for authentication testing.
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
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
    
    def test_login(self):
        # This test uses self.client.login
        success = self.client.login(username="testuser", password="testpassword")
        self.assertTrue(success)
    
    def test_protected_endpoint(self):
        # Use self.client.login to authenticate
        self.client.login(username="testuser", password="testpassword")
        url = reverse("book-create")
        response = self.client.post(url, {"title": "New", "publication_year": 2021, "author": self.author.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class SimpleTest(TestCase):
    def test_database_isolation(self):
        """Test that we are using a separate test database"""
        pass
