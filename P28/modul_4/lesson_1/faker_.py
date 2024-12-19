from dataclasses import dataclass

import psycopg2
import faker

from P28.modul_4.lesson_1.py_pg import PG

f = faker.Faker()
for i in range(1000):
    print(f.first_name())
    print(f.last_name())
    print(f.user_name())
    print(f.email())

@dataclass
class User(PG):
    id : int = None
    first_name : str = None
    last_name : str = None
    username : str = None
    email : str = None
    age : int = None

f = faker.Faker()
counter = 0
while counter < 1000:
    user_fake = {
        "first_name" : f.first_name(),
        "last_name" : f.last_name(),
        "username" : f.user_name(),
        "email" : f.email(),
        "age" : f.random_int(11 , 99),
    }
    user = User(username=user_fake.get('username')).objects()
    if not user:
        User(**user_fake).save()
        counter += 1
