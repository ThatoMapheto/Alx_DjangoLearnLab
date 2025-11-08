# Update Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")

# Verify the update
updated_book = Book.objects.get(id=book.id)
print(f"Verified title: {updated_book.title}")