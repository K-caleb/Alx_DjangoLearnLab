# Create Operation

from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)

# Retrieve Operation

books = Book.objects.all()
for b in books:
print(b.title, b.author, b.publication_year)

# Update Operation

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
updated_book = Book.objects.get(id=book.id)
print(updated_book.title)

# Delete Operation

book.delete()
books_after_delete = Book.objects.all()
print(books_after_delete)