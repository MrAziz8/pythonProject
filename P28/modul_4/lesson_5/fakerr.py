import psycopg2
from faker import Faker
import random

connection = psycopg2.connect(
    dbname="ecommerce",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()


cursor.execute("""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    join_date DATE
)
""")

cursor.execute("""
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    stock INT
)
""")

cursor.execute("""
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT,
    product_id INT,
    order_date DATE,
    quantity INT,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
)
""")
connection.commit()

faker = Faker()

def generate_fake_users(batch_size=1000, total_records=100000):
    for _ in range(0, total_records, batch_size):
        users = [
            (
                faker.name(),
                faker.unique.email(),
                faker.date_this_decade()
            )
            for _ in range(batch_size)
        ]
        cursor.executemany("INSERT INTO users (name, email, join_date) VALUES (%s, %s, %s)", users)
        connection.commit()

def generate_fake_products(batch_size=1000, total_records=50000):
    for _ in range(0, total_records, batch_size):
        products = [
            (
                faker.word().capitalize(),
                round(random.uniform(5, 1000), 2),
                random.randint(1, 500)
            )
            for _ in range(batch_size)
        ]
        cursor.executemany("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", products)
        connection.commit()

def generate_fake_orders(batch_size=1000, total_records=1000000):
    for _ in range(0, total_records, batch_size):
        orders = [
            (
                random.randint(1, 100000),
                random.randint(1, 50000),
                faker.date_this_year(),
                random.randint(1, 10)
            )
            for _ in range(batch_size)
        ]
        cursor.executemany("INSERT INTO orders (user_id, product_id, order_date, quantity) VALUES (%s, %s, %s, %s)", orders)
        connection.commit()

print("Fake ma'lumotlarni kiritish boshlandi...")
print("Foydalanuvchilarni kiritish...")
generate_fake_users()
print("Mahsulotlarni kiritish...")
generate_fake_products()
print("Buyurtmalarni kiritish...")
generate_fake_orders()
print("Ma'lumotlar kiritildi.")

cursor.close()
connection.close()
