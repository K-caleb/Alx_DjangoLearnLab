# Retrieve all Book instances
books = Book.objects.all()
for b in books:
    print(b.title, b.author, b.publication_year)
# Expected output:
# 1984 George Orwell 1949
