import psycopg2
from faker import Faker
import random

# PostgreSQL ma'lumotlar bazasiga ulanish
connection = psycopg2.connect(
    dbname="education",  # Bazangiz nomini o'zgartiring
    user="postgres",
    password="1",  # Parolni o'zgartiring
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

# Faker kutubxonasini ishga tushirish
faker = Faker()

# Subject jadvali uchun ma'lumotlarni kiritish
subjects = ["Mathematics", "Science", "History", "Literature", "Art", "Geography", "Computer Science", "Music", "Physical Education", "Philosophy"]
cursor.executemany("INSERT INTO subject (name) VALUES (%s)", [(subject,) for subject in subjects])
connection.commit()

# Subject jadvalidan ma'lumotlarni olish
cursor.execute("SELECT id, name FROM subject")
subjects_db = cursor.fetchall()

# Teachers jadvali uchun ma'lumotlarni kiritish
teachers_data = []
for _ in range(10000):
    teacher_name = faker.name()
    subject = random.choice(subjects_db)[0]  # Tasodifiy predmet tanlash
    experience_years = random.randint(1, 40)
    teachers_data.append((teacher_name, subject, experience_years))

cursor.executemany("INSERT INTO teachers (name, subject, experience_years) VALUES (%s, %s, %s)", teachers_data)
connection.commit()

# Students jadvali uchun ma'lumotlarni kiritish
students_data = []
for _ in range(100000):
    student_name = faker.name()
    student_class = random.choice(["1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade", "6th Grade", "7th Grade", "8th Grade", "9th Grade", "10th Grade", "11th Grade", "12th Grade"])
    enrollment_date = faker.date_this_decade()
    students_data.append((student_name, student_class, enrollment_date))

cursor.executemany("INSERT INTO students (name, class, enrollment_date) VALUES (%s, %s, %s)", students_data)
connection.commit()

# Grades jadvali uchun ma'lumotlarni kiritish
grades_data = []
for _ in range(100000):
    student_id = random.randint(1, 10000)
    subject_id = random.randint(1, 10)  # 10 ta predmetdan birini tanlash
    grade = random.choice(["A", "B", "C", "D", "E", "F"])
    grade_date = faker.date_this_year()
    grades_data.append((student_id, subject_id, grade, grade_date))

cursor.executemany("INSERT INTO grades (student_id, subject, grade, date) VALUES (%s, %s, %s, %s)", grades_data)
connection.commit()

cursor.close()
connection.close()

print("Fake ma'lumotlar kiritildi.")
