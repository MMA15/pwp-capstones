##User class object
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("New email updated to: " + self.email)

    def __repr__(self):
        return "User " + self.name + " has the email " + self.email + " inputed into the system. They have read " + str(len(self.books)) + " books."

    def __eq__(self, other_user):
        return ((self.name == other_user.name) and (self.email == other_user.email))

    def read_book(self, book, rating = None):
        if rating == None or ((rating >= 0) and (rating <= 4)):
            self.books[book] = rating
        else:
            return print("Invalid rating, please try again.")

#average rating based on the users inputs for all books
    def get_average_rating(self):
        total = 0
        new_values = []
        for rating in self.books.values():
            if rating != None:
                new_values.append(rating)
        for value in new_values:
            total +=value
        if len(new_values) == 0:
            return 0
        else:
            return total/len(new_values)

##Book class objectB
class Book(object):

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        #changing the isbn actually changes the hash of the object since this attribute
        #is being used to create the hash. Both Title and Isbn should be immutable
        #in order to make the Book object immutable.
        #But if we can change Isbn, it means its mutable now.
        self.isbn = new_isbn
        print(self.title + " isbn has been updated to " + str(self.isbn))

    def add_rating(self, rating):
        if rating == None or ((rating >= 0) and (rating <= 4)):
            self.ratings.append(rating)
        else:
            return print("Invalid rating, please try again.")

    def __eq__(self, other_book):
        return ((self.title == other_book.title) and (self.isbn == other_book.isbn))

    def __hash__(self):
        return hash((self.title, self.isbn))

#average rating for one specific book
    def get_average_rating(self):
        total = 0
        new_values = []
        for rating in self.ratings:
            if rating != None:
                new_values.append(rating)
        for value in new_values:
            total += value
        if len(new_values) == 0:
            return 0
        else:
            return total/len(new_values)

    def __repr__(self):
        return self.title

##Fiction class, subClass of Book
class Fiction(Book):

    def __init__(self, title, author, isbn):
        super().__init__(title,isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return self.title + " by " + self.author

##Fiction class, subClass of Book
class Non_Fiction(Book):

    def __init__(self, title, subject, level, isbn):
        super().__init__(title,isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return self.title + ", a " + self.level + " manual on " + self.subject

##TomeRater class, used to interconnect Book and User objects.
class TomeRater(object):

    def __init__(self):
        self.users = {}
        self.books = {}

    def isbn_check (self, added_book):
    #confirming the isbn of the book object is not the same as any other book
    #only if there is more than one book in the system
        if len(self.books) > 1:
            for book in self.books:
                if (added_book != book) and (added_book.get_isbn() == book.get_isbn()):
                    removed_book = self.books.pop(added_book)
                    removed_book_from_user = self.users[email].books.pop(added_book)
                    print("The isbn " + str(book.get_isbn()) + " exists somewhere else. Please confirm")
                    break

    def create_book(self, title, isbn):
        new_book = Book(title, isbn)
        return new_book

    def create_novel(self, title, author, isbn):
        new_fiction_novel = Fiction(title, author, isbn)
        return new_fiction_novel

    def create_non_fiction(self, title, subject, level, isbn):
        new_non_fiction = Non_Fiction(title, subject, level, isbn)
        return new_non_fiction

##it made more sense to have add user first before adding a book to the user
    def add_user(self, name, email, user_books = None):
        characters = ["@", ".com", ".edu", ".org"]
        for item in characters:
            if email.find(item) > 0:
                if email in self.users.keys():
                    return print("This user already exits!")
                else:
                    new_user = User(name, email)
                    self.users[new_user.email] = new_user

                if user_books != None:
                    for book in user_books:
                        self.add_book_to_user(book, email)
                return new_user
            else:
                return print("Invalid email")

    def add_book_to_user(self, book, email, rating = None):
        if email in self.users:

            self.users[email].read_book(book, rating)
            book.add_rating(rating)

            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
                self.isbn_check(book) # only check when initially adding
        else:
            print("No user with email " + email)

    def print_catalog(self):
        for key in self.books.keys():
            print(key)

    def print_users(self):
        for value in self.users.values():
            print(value)

    def highest_rated_book(self):
        highest_rating = 0
        highest_book = None

        for book in self.books.keys():
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                highest_book = book
        return highest_book

    def most_positive_user(self):
        highest_rating = 0
        positive_user = None

        for user in self.users.values():
            if user.get_average_rating() > highest_rating:
                highest_rating = user.get_average_rating()
                positive_user = user
        return positive_user

    def get_most_read_book(self, n):
        ordered_list = []

        while len(ordered_list) < len(self.books):
            highest_count = 0
            highest_book = None

            for book in self.books:
                if book.get_title() in ordered_list:
                    continue
                elif self.books[book] > highest_count:
                    highest_count = self.books[book]
                    highest_book = book

            #in the add_book_to_user method, the book starts off with a count of 1 when it is added to the user. so there should be no books with 0.
            if highest_count == 0:
                pass
            else:
                ordered_list.append(highest_book.get_title())

        return ordered_list[:n]

    def get_most_profilic_reader(self, n):
        ordered_list = []

        while len(ordered_list) < len(self.users):
            highest_count = 0
            highest_user = None

            for user_email in self.users:
                if self.users[user_email].name in ordered_list:
                    continue
                elif len(self.users[user_email].books) > highest_count:
                    highest_count = len(self.users[user_email].books)
                    highest_user = self.users[user_email]

            if highest_count == 0:
                pass
            else:
                ordered_list.append(highest_user.name)

        return ordered_list[:n]

    def __repr__(self):
        return "This database contains: {users} Users and {books} Books".format(users = len(self.users), books = len(self.books))
