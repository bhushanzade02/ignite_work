# from fastapi import FastAPI, HTTPException
# import mysql.connector
# from mysql.connector import Error
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# app = FastAPI(title="Project Gutenberg Books API")

# # Database connection
# def get_connection():
#     try:
#         conn = mysql.connector.connect(
#             host=os.getenv("DB_HOST"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             database=os.getenv("DB_NAME"),
#             port=os.getenv("DB_PORT")
#         )
#         return conn
#     except Error as e:
#         print("Error while connecting to MySQL", e)
#         return None


# @app.get("/books")
# def get_books(limit: int = 50):
#     """
#     Retrieve books with author, language, bookshelf, and format info.
#     """
#     query = """
#     SELECT 
#         b.id AS book_id,
#         b.title,
#         b.gutenberg_id,
#         b.download_count,
#         b.media_type,
#         GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS authors,
#         GROUP_CONCAT(DISTINCT l.code SEPARATOR ', ') AS languages,
#         GROUP_CONCAT(DISTINCT bs.name SEPARATOR ', ') AS bookshelves,
#         GROUP_CONCAT(DISTINCT f.url SEPARATOR ', ') AS download_links
#     FROM books_book b
#     LEFT JOIN books_book_authors ba ON b.id = ba.book_id
#     LEFT JOIN books_author a ON ba.author_id = a.id
#     LEFT JOIN books_book_languages bl ON b.id = bl.book_id
#     LEFT JOIN books_language l ON bl.language_id = l.id
#     LEFT JOIN books_book_bookshelves bbs ON b.id = bbs.book_id
#     LEFT JOIN books_bookshelf bs ON bbs.bookshelf_id = bs.id
#     LEFT JOIN books_format f ON b.id = f.book_id
#     GROUP BY b.id, b.title, b.gutenberg_id, b.download_count, b.media_type
#     ORDER BY b.download_count DESC
#     LIMIT %s;
#     """

#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     cursor = conn.cursor(dictionary=True)
#     cursor.execute(query, (limit,))
#     result = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return {"total_books": len(result), "books": result}
from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
import os

app = FastAPI(title="Project Gutenberg Books API")

# ✅ Database connection function
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),
            user=os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE"),
            port=int(os.getenv("MYSQLPORT", 3306))
        )
        return conn
    except Error as e:
        print("❌ Error while connecting to MySQL:", e)
        return None


@app.get("/")
def root():
    return {"message": "API is running successfully 🚀"}


@app.get("/books")
def get_books(limit: int = 50):
    """
    Retrieve books with author, language, bookshelf, and format info.
    """
    query = """
    SELECT 
        b.id AS book_id,
        b.title,
        b.gutenberg_id,
        b.download_count,
        b.media_type,
        GROUP_CONCAT(DISTINCT a.name SEPARATOR ', ') AS authors,
        GROUP_CONCAT(DISTINCT l.code SEPARATOR ', ') AS languages,
        GROUP_CONCAT(DISTINCT bs.name SEPARATOR ', ') AS bookshelves,
        GROUP_CONCAT(DISTINCT f.url SEPARATOR ', ') AS download_links
    FROM books_book b
    LEFT JOIN books_book_authors ba ON b.id = ba.book_id
    LEFT JOIN books_author a ON ba.author_id = a.id
    LEFT JOIN books_book_languages bl ON b.id = bl.book_id
    LEFT JOIN books_language l ON bl.language_id = l.id
    LEFT JOIN books_book_bookshelves bbs ON b.id = bbs.book_id
    LEFT JOIN books_bookshelf bs ON bbs.bookshelf_id = bs.id
    LEFT JOIN books_format f ON b.id = f.book_id
    GROUP BY b.id, b.title, b.gutenberg_id, b.download_count, b.media_type
    ORDER BY b.download_count DESC
    LIMIT %s;
    """

    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (limit,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"total_books": len(result), "books": result}
