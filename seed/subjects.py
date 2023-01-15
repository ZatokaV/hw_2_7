from faker import Faker
from random import randint

from database.db import session
from database.models import Subject

fake = Faker('uk_UA')
TEACHERS = 4
SUBJECTS = 7


def create_subjects():
    for _ in range(SUBJECTS):
        subject = Subject(
            subject_name=fake.job(),
            teacher_id=randint(1, TEACHERS)
        )
        session.add(subject)
    session.commit()


if __name__ == '__main__':
    create_subjects()
