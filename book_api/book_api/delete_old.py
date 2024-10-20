from books.models import Book, Author

# Identify invalid books
invalid_books = Book.objects.filter(author__isnull=True)
print("Invalid books:", invalid_books)

# Option 1: Update invalid entries to a valid author
valid_author = Author.objects.first()  # Replace with a valid author instance
for book in invalid_books:
    book.author = valid_author
    book.save()

# Option 2: Delete invalid entries
# invalid_books.delete()

# Exit the shell
exit()