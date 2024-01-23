from fastapi import FastAPI,Body

app = FastAPI()

#list of dictionaries
BOOKS = [
    {'title' : 'one','author' : 'one', 'category' : 'science'},
    {'title' : 'two','author' : 'two', 'category' : 'maths'},
    {'title' : 'three','author' : 'three', 'category' : 'science'},
    {'title' : 'four','author' : 'four', 'category' : 'computer'},
    {'title' : 'five','author' : 'five', 'category' : 'english'},
    {'title' : 'six','author' : 'two', 'category' : 'science'}
    ]

@app.get("/books")
async def read_all_books():
    return BOOKS 

@app.get("/books/mybook")
async def read_all_books():
    return {'book_title':'My fav book!'} 

#To get a single book out of the list of books based on book title that we're passing in as a path parameter.
@app.get("/books/{book_title}")
async def read_all_books(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        
@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

#To get all books written by a specific author
@app.get("/books/byauthor/{book_author}")
async def read_author_category_by_query(book_author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author') == book_author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author:str,category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author') == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.remove(BOOKS[i])
            break


# @app.get("/books/{dynamic_param}")
# async def read_all_books(dynamic_param: str):
#     return {'dynamic_param':dynamic_param}

#static parameter functions should be before the dynamic ones as fast API looks at all the 
#functions in a chronological order from top to bottom
# @app.get("/books/mybook")
# async def read_all_books():
#     return {'book_title':'My fav book!'} 