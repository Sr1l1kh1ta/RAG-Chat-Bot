import core
from typing import List

class Book(core.Resource):
    def __init__(self,isbn,title,author,publication_year,available):
        super().__init__(name=title, created_at=publication_year)
        self.isbn = isbn
        self.author = author
        self.title = title
        self.publication_year = publication_year
        self._available = available

    @property
    def available(self) -> bool:
        return self._available

    @available.setter
    def available(self, available: bool):
        self._available = available

    def allocate(self):
        if self._available == True:
            self._available = False
            return True
        return False
    
    def release(self):
        self._available = True

    def get_status(self):
        return self._available
        
        
class Member(core.user):
    def __init__(self,id,name,role,contact_info):
        super().__init__(user_id=id, name=name, role=role)
        self._contact_info = contact_info
        self._borrowed_books = []


    @property
    def contact_info(self) -> str:
        return self._contact_info

    @property
    def borrowed_books(self) -> List[Book]:
        return self._borrowed_books

    def request_resource(self, book_title):
        for i in Librarian.catalog:
            if Librarian.catalog[i].title == book_title:
                book = Librarian.catalog[i]
        if book.allocate():
            self._borrowed_books.append(book)
        else:
            print("Not available")

    def return_resource(self, book_title):
        for i in Librarian.catalog:
            if Librarian.catalog[i].title == book_title:
                book = Librarian.catalog[i]
        book.release()
        self._borrowed_books.remove(book)

    def view_status(self,book_title):
        for i in Librarian.catalog:
            if Librarian.catalog[i].title == book_title:
                book = Librarian.catalog[i]
        return book.get_status()
        


class Librarian(core.user):
    catalog = {}
    def __init__(self, user_id, name, role) -> None:
        super().__init__(user_id, name, role)
        self.members = {}
        self.MAX_BOOKS_PER_MEMBER = 5
        self.LOAN_DURATION_DAYS = 14

    def add_book(self, book: Book):
        Librarian.catalog[book.isbn] = book

    def remove_book(self, isbn: str):
        Librarian.catalog.pop(isbn, None)

    def get_book(self, book_title: str) -> Book:
        for i in Librarian.catalog:
            if Librarian.catalog[i].title == book_title:
                isbn = i
                return Librarian.catalog.get(isbn)
            else:
                print("Not found")
                pass

    def register_member(self, member: Member):
        self.members[member.user_id] = member

    def unregister_member(self, user_id: str):
        self.members.pop(user_id, None)

    def get_member(self, user_id: str) -> Member:
        return self.members.get(user_id)

    def request_resource(self, user_id: str, book_title: str):
        member = self.get_member(user_id)
        print(member)
        book = self.get_book(book_title)
        print(book)

        if member and book and book._available:
            if len(member.borrowed_books) < self.MAX_BOOKS_PER_MEMBER:
                member.request_resource(book.title)
                book._available = False
                print(f"Book borrowed: {book.title} by {member.name}")
            else:
                print(f"Member {member.name} has reached the maximum number of borrowed books.")
        else:
            print("Book or member not found, or book is not available.")

    def return_resource(self, member_id: str, book_title: str):
        member = self.get_member(member_id)
        book = self.get_book(book_title)

        if member and book:
            member.return_resource(book.title)
            book._available = True
            print(f"Book returned: {book.title} by {member.name}")
        else:
            print("Book or member not found.")

    def view_status(self,book_title):
        for i in Librarian.catalog:
            if Librarian.catalog[i].title == book_title:
                book = Librarian.catalog[i]
        return book.get_status()

    def search_books(self, keyword: str) -> List[Book]:
        matching_books = [book for book in Librarian.catalog.values() if keyword in book.title or keyword in book.author]
        return matching_books
