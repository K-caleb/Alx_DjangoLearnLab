# Delete the book
book.delete()

# Confirm deletion
books_after_delete = Book.objects.all()
print(books_after_delete)
# Expected output: <QuerySet []>
