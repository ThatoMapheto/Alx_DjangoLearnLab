from relationship_app.models import Author, Book, Library, Librarian
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()


def query_all_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")
        return []


def list_all_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
        return []


def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print(f"Librarian for '{library_name}' not found")
        return None


# Example usage
if __name__ == "__main__":
    # Create sample data
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")

    book1 = Book.objects.create(
        title="Harry Potter", author=author1, publication_year=1997)
    book2 = Book.objects.create(
        title="1984", author=author2, publication_year=1949)

    library = Library.objects.create(name="City Central Library")
    library.books.add(book1, book2)

    librarian = Librarian.objects.create(name="Alice Johnson", library=library)

    # Run queries
    query_all_books_by_author("J.K. Rowling")
    list_all_books_in_library("City Central Library")
    get_librarian_for_library("City Central Library")
