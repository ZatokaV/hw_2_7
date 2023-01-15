from faker import Faker
from random import randint

from database.db import session
from database.models import Grade

fake = Faker('uk_UA')
TEACHERS = 4
SUBJECTS = 7
STUDENTS = 40
GRADES = 20


def create_grades():
    for _ in range(STUDENTS * GRADES):
        grade = Grade(
            grades=randint(1, 12),
            student_id=randint(1, STUDENTS),
            subject_id=randint(1, SUBJECTS),
            lesson_date=fake.date_between(start_date='-1y')
        )
        session.add(grade)
    session.commit()


if __name__ == '__main__':
    create_grades()