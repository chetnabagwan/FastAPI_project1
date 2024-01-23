from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status

app=FastAPI()

class Book:
    id:int
    title:str
    author:str  
    description:str 
    rating:int
    published_date:int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date

class BookRequest(BaseModel):
    id:Optional[int] = Field(title='id is not needed')
    title:str = Field(min_length=1)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=0, lt=6)
    published_date:int = Field(gt=1999,lt=2031)

    class Config:
        json_schema_extra = {
            'example':{
                'title':'a',
                'author':'ab',
                'description':'abc',
                'rating': 4,
                'published_date':2024
            }
        }
    
#Books list in which we have book objects in it
BOOKS =[
    Book(1,'Computer Science','Sam','Nice book',5,2021),
    Book(2,'Science','Ram','good book',4,2014),
    Book(3,'English','Joy','Informative',5,2010),
    Book(4,'FastAPI','Alex','great book',5,2013),
    Book(5,'JAVA','Harry','Java beginner to advanced',5,2023),
]

#fetch all books
@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

#fetch a book by book_id,path parameter locates a specific resource
@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')

#fetch a book by book rating, query parameter filters the book by book rating,
@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int=Query(gt=0)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

#fetch books filtered by published date
@app.get("/books/update/",status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

#with data validation
@app.post("/createbook",status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

#update a book
@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i]=book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')    


#delete a book
@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Book not found')    


