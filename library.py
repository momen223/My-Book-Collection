import json
from typing import List, Optional, Dict, Any

BOOKS_FILE = 'data.json'

def load_books() -> List[Dict[str, Any]]:
    try:
        with open(BOOKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_books(books: List[Dict[str, Any]]) -> None:
    try:
        with open(BOOKS_FILE, 'w') as file:
            json.dump(books, file, indent=4)
    except IOError as e:
        print(f"Error saving books: {e}")

def add_book(books: List[Dict[str, Any]], title: str, author: str, genre: str, year: int, status: str) -> None:
    if any(book['title'] == title for book in books):
        print(f"A book with the title '{title}' already exists.")
        return

    book = {
        'title': title,
        'author': author,
        'genre': genre,
        'year': year,
        'status': status
    }
    books.append(book)
    save_books(books)

def list_books(books: List[Dict[str, Any]], filter_by: Optional[str] = None, value: Optional[Any] = None) -> None:
    filtered_books = [book for book in books if filter_by is None or book.get(filter_by) == value]
    for book in filtered_books:
        print(f"Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}, Year: {book['year']}, Status: {book['status']}")

def update_book(books: List[Dict[str, Any]], title: str, **updates: Any) -> bool:
    for book in books:
        if book['title'] == title:
            book.update(updates)
            save_books(books)
            return True
    return False

def delete_book(books: List[Dict[str, Any]], title: str) -> None:
    books = [book for book in books if book['title'] != title]
    save_books(books)

def main():
    books = load_books()
    
    while True:
        print("\nBook Manager")
        print("1. Add Book")
        print("2. List Books")
        print("3. Update Book")
        print("4. Delete Book")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            genre = input("Enter genre: ")
            try:
                year = int(input("Enter year: "))
            except ValueError:
                print("Invalid year. Please enter a number.")
                continue
            status = input("Enter status (e.g., read, unread): ")
            add_book(books, title, author, genre, year, status)
        
        elif choice == '2':
            filter_by = input("Enter filter field (or leave empty): ")
            if filter_by:
                value = input(f"Enter filter value for '{filter_by}' (or leave empty): ")
                list_books(books, filter_by if filter_by else None, value if value else None)
            else:
                list_books(books)
        
        elif choice == '3':
            title = input("Enter the title of the book to update: ")
            field = input("Enter field to update (e.g., author, genre, year, status): ")
            new_value = input("Enter new value: ")
            if field == "year":
                try:
                    new_value = int(new_value)
                except ValueError:
                    print("Invalid year. Please enter a number.")
                    continue
            if update_book(books, title, **{field: new_value}):
                print("Book updated successfully.")
            else:
                print("Book not found.")
        
        elif choice == '4':
            title = input("Enter the title of the book to delete: ")
            delete_book(books, title)
            print("Book deleted successfully.")
        
        elif choice == '5':
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    
    print("Exiting Book Manager.")

if __name__ == "__main__":
    main()
