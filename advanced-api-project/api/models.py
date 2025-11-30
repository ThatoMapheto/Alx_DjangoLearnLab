from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.

    Fields:
    - name: CharField to store the author's full name
    """
    name = models.CharField(
        max_length=200, help_text="Full name of the author")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model representing a published book.

    Fields:
    - title: CharField for the book's title
    - publication_year: IntegerField for the year of publication
    - author: ForeignKey linking to the Author model (one-to-many relationship)
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    publication_year = models.IntegerField(
        help_text="Year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="Author of the book"
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author.name}"
