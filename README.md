# LibrarySystem
Library Management System
Here's a concise README file for your library management system:

# Library Management System

## Project Overview
A desktop application built with Python and Tkinter for managing book inventory in libraries. The system provides essential book management features with a simple graphical interface.

## Key Features
- Add new books to the library database
- Update existing book information
- Delete books from the system
- Search books by title or author
- Track book availability status (Available/Issued)
- View all books in an organized table view

## Technical Details
- **Programming Language**: Python 3
- **GUI Framework**: Tkinter
- **Database**: SQLite (built-in)
- **Components Used**:
  - ttk for styled widgets
  - SQLite3 for data storage
  - Tkinter message boxes for alerts

## Getting Started
1. Ensure Python 3 is installed on your system
2. Download or clone the project files
3. Run the application:
   ```bash
   python library_management.py
   ```

## How to Use
1. **Add Books**: Fill in the book details in the left panel and click "Add Book"
2. **Modify Records**: Select a book from the table to update or delete
3. **Search**: Use the search function to find specific books
4. **Status Tracking**: Change book status between Available and Issued

## Database Information
The system uses a SQLite database (library.db) with the following structure:
- BK_NAME (Book title)
- BK_ID (Unique identifier)
- AUTHOR_NAME
- BK_STATUS (Available/Issued)
- CARD_ID (If issued)

The application comes preloaded with sample book data for demonstration purposes.
