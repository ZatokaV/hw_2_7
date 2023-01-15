from faker import Faker
from random import randint

from database.db import session
from database.models import Student

fake = Faker('uk_UA')
GROUPS = 3
STUDENTS = 40


def create_students():
    for _ in range(40):
        student = Student(
            name=fake.name(),
            team_id=randint(1, GROUPS)
        )
        session.add(student)
    session.commit()


if __name__ == '__main__':
    create_students()
