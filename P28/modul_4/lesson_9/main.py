import psycopg2
from faker import Faker
import random

connection = psycopg2.connect(
    dbname="cinema",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

cursor.execute("""
create table movies (
    id serial primary key,
    title varchar(255) ,
    genre TEXT ,
    release_year integer
)
""")
connection.commit()

faker = Faker()
genres = ["Action", "Comedy", "Drama", "Horror"]

def generate_fake_movies(batch_size=1000, total_records=500000):
    for _ in range(0, total_records, batch_size):
        movies = [
            (
                faker.text(max_nb_chars=20).strip(),
                random.choice(genres),
                random.randint(1950, 2023)
            )
            for _ in range(batch_size)
        ]
        cursor.executemany("INSERT INTO movies (title, genre, release_year) VALUES (%s, %s, %s)", movies)
        connection.commit()

print("Fake ma'lumotlarni kiritish boshlandi...")
generate_fake_movies()
print("Ma'lumotlar kiritildi.")

cursor.close()
connection.close()
