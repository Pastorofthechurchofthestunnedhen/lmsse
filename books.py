from database import CursorFromConnectionFromPool
from isbn_maker import makefunc as isbn_creator


class Books:
    def __init__(self, isbn, copy_no, name, author, language, publisher, branch_id):
        self.isbn = isbn
        self.copy_no = copy_no
        self.author = author
        self.name = name
        self.language = language
        self.publisher = publisher
        self.issued_by = 0
        self.branch_id = branch_id

    def __repr__(self):
        return "Book: \n{}\n{} {}\n{}\n{}".format(self.isbn,
                                                  self.name,
                                                  self.author,
                                                  self.publisher,
                                                  self.language)

    def newcopy(self, isbn):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select COUNT(*) FROM public.books where isbn=%s;", (isbn,))
            rowcount = cursor.fetchone()[0]
            return rowcount

    def newisbn(self, name, author, publisher, language):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                "select count(*) from public.books where name=%s and author=%s and publisher=%s and language=%s;",
                (name, author, publisher, language))
            rowcount = cursor.fetchone()[0]
            if rowcount == 0:
                self.isbn = isbn_creator()
            else:
                with CursorFromConnectionFromPool() as cursor:
                    cursor.execute(
                        'select * from public.books where name=%s and author=%s and publisher=%s and language=%s;',
                        (name, author, publisher, language))
                    user_data = cursor.fetchone()
                    self.isbn = user_data[0]

    def new_book(self):
        self.newisbn(self.name, self.author, self.publisher, self.language)
        self.copy_no = (self.newcopy(self.isbn)) + 1
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                "insert into public.books(isbn,copy_no,name,author,language,publisher,issued_by,branch_id) values(%s,%d,%s,%s,%s,%s,0);",
                (self.isbn, self.copy_no, self.name, self.author, self.language, self.publisher))

    def deletebook(self, isbn, copy_no):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("delete from public.books where books_pkey=%s;", (str(isbn) + str(copy_no)))

    @classmethod
    def search(cls, name, isbn, author, language, publisher):
        query = "select * from public.books where "
        count = 0
        if name != None:
            if count != 0:
                query = query + "and "
            query = query + "name like %{}% ".format(name)
        if isbn != None:
            if count != 0:
                query = query + "and "
            query = query + "isbn=%s ", (isbn,)
        if author != None:
            if count != 0:
                query = query + "and "
            query = query + "author like %{}% ".format(author)
        if language != None:
            if count != 0:
                query = query + "and "
            query = query + "language=%s ", (language,)
        if publisher != None:
            if count != 0:
                query = query + "and "
            query = query + "publisher like %{}% ".format(publisher)
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(query)
            user_data = cursor.fetchall()
        return user_data
