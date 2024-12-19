import random
from dataclasses import dataclass
from datetime import date, timedelta

import faker

from module_4.lesson_2.py_pg import PG

f = faker.Faker()

@dataclass
class User(PG):
    id : int = None
    first_name : str = None
    last_name : str = None
@dataclass
class Author(PG):
    id : int = None
    first_name : int = None
    last_name : int = None
    birthdate: str = None
    address: str = None

@dataclass
class Card(PG):
    id : int = None
    card_number : int = None
    user_id : int = None


@dataclass
class Genre(PG):
    id : int = None
    name : str = None

@dataclass
class Book(PG):
    id : int = None
    title : str = None
    description : str = None
    author_id : int = None
    genre_id : int = None

@dataclass
class Rent(PG):
    user_id : int = None
    book_id : int = None
    start_at : str = None
    end_at : str = None
    status : bool = None

def users_fixtures(count = 0):
    counter = 0
    while counter < count:
        new_user = {
            "first_name" : f.first_name(),
            "last_name" : f.last_name(),
        }
        User(**new_user).save()
        counter += 1


def authors_fixtures(count = 0):
    counter = 0
    while counter < count:
        new_author = {
            "first_name" : f.first_name(),
            "last_name" : f.last_name(),
            "birthdate" : f.date_of_birth(minimum_age=24),
            "address" : f.address()
        }
        Author(**new_author).save()
        counter += 1


def cards_fixtures(count=1):
    counter = 1
    while counter <= count:
        new = {
            "card_number": 1000+counter,
            "user_id": counter,
        }
        Card(**new).save()
        counter += 1



def genres_fixtures():
    for i in ["ilmiy" , 'badiiy' , 'ertak' , 'fantastic' , 'dramma' , 'trigger']:
        Genre(name=i).save()


def books_fixtures(count=0):
    counter = 1
    while counter <= count:
        new = {
            "title": f.name(),
            "description": f.text(),
            "author_id": f.random_int(1, 200),
            "genre_id": f.random_int(1, 6),
        }
        Book(**new).save()
        counter += 1


def rents_fixtures(count=0):
    counter = 1
    while counter <= count:
        start_at = date.fromisoformat(str(f.date_of_birth(minimum_age=0,maximum_age=9)))
        new = {
            "user_id": f.random_int(1, 1000),
            "book_id": f.random_int(1, 5000),
            "start_at": start_at,
            "end_at": start_at + timedelta(7),
            "status": random.choice([True , False]),
        }
        Rent(**new).save()
        counter += 1
