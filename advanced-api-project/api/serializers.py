from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model that handles all fields and includes custom validation.

    Fields:
    - id: Primary key (read-only)
    - title: Book title
    - publication_year: Year of publication with custom validation
    - author: Foreign key to Author model

    Validation:
    - Custom validation for publication_year to ensure it's not in the future
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Validate that the publication year is not in the future.

        Args:
            value (int): The publication year to validate

        Returns:
            int: The validated publication year

        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model that includes nested BookSerializer.

    Fields:
    - id: Primary key (read-only)
    - name: Author's name
    - books: Nested serialization of related Book objects (read-only)

    The nested relationship allows serializing author data along with their books
    in a single API response, providing a hierarchical data structure.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
