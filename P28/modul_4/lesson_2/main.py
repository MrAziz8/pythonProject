import psycopg2
from faker import Faker
import random
from datetime import timedelta

# PostgreSQL ulanishi
conn = psycopg2.connect(
    dbname="lesson_3",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

faker = Faker()

# Authors jadvaliga 1000 ta yozuv kiritish
def insert_authors(count=1000):
    authors = [
        (
            faker.first_name(),
            faker.last_name(),
            faker.date_of_birth(minimum_age=25, maximum_age=80),
            faker.address()
        )
        for _ in range(count)
    ]
    cursor.executemany(
        "INSERT INTO authors (first_name, last_name, birthdate, address) VALUES (%s, %s, %s, %s)",
        authors
    )
    print(f"{count} mualliflar kiritildi.")

# Books jadvaliga 1000 ta yozuv kiritish
def insert_books(count=1000):
    cursor.execute("SELECT id FROM authors")
    author_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM genres")
    genre_ids = [row[0] for row in cursor.fetchall()]

    books = [
        (
            faker.sentence(nb_words=4),
            faker.text(max_nb_chars=200),
            random.choice(author_ids),
            random.choice(genre_ids)
        )
        for _ in range(count)
    ]
    cursor.executemany(
        "INSERT INTO books (title, description, author_id, genre_id) VALUES (%s, %s, %s, %s)",
        books
    )
    print(f"{count} kitoblar kiritildi.")

# Rents jadvaliga 1000 ta yozuv kiritish
def insert_rents(count=1000):
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM books")
    book_ids = [row[0] for row in cursor.fetchall()]

    rents = [
        (
            random.choice(user_ids),
            random.choice(book_ids),
            (start_at := faker.date_between(start_date="-30d", end_date="today")),
            start_at + timedelta(days=random.randint(7, 30)),
            random.choice([True, False])
        )
        for _ in range(count)
    ]
    cursor.executemany(
        "INSERT INTO rents (user_id, book_id, start_at, end_at, status) VALUES (%s, %s, %s, %s, %s)",
        rents
    )
    print(f"{count} ijaralar kiritildi.")

# Ma'lumotlarni qo'shish
try:
    insert_authors(1000)  # Authors jadvaliga 1000 ta yozuv
    insert_books(1000)   # Books jadvaliga 1000 ta yozuv
    insert_rents(1000)   # Rents jadvaliga 1000 ta yozuv

    conn.commit()  # O'zgarishlarni saqlash
except Exception as e:
    print("Xatolik yuz berdi:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()
