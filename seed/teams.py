from faker import Faker

from database.db import session
from database.models import Team

fake = Faker('uk_UA')
TEAMS = 3


def create_teams():
    for i in range(TEAMS):
        team = Team(
            team_name=f'team{i}'
        )
        session.add(team)
    session.commit()


if __name__ == '__main__':
    create_teams()
