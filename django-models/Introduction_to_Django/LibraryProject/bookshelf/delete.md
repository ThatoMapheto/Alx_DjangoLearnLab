# Delete Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Verify deletion
book_count = Book.objects.count()
print(f"Total books in database: {book_count}")

# Confirm deletion by trying to retrieve
try:
    Book.objects.get(title="Nineteen Eighty-Four")
    print("Book still exists")
except Book.DoesNotExist:
    print("Book successfully deleted - no longer in database")