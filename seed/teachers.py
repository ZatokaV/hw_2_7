from faker import Faker

from database.db import session
from database.models import Teacher

fake = Faker('uk_UA')


def create_teachers():
    for _ in range(4):
        teacher = Teacher(
            name=fake.name()
        )
        session.add(teacher)
    session.commit()


if __name__ == '__main__':
    create_teachers()
    