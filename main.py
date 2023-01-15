from datetime import datetime

from sqlalchemy import func, desc, and_

from database.db import session
from database.models import Subject, Student, Grade, Teacher, Team


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def query_1():
    result = session.query(
        Student.name,
        func.round(func.avg(Grade.grades), 2).label('avg_grade')
    ).select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    print('Студенти з найвищим середнім балом')
    for tuples in result:
        print(f'Студент: {tuples[1]}, Бал: {tuples[0]}')


# Знайти студента із найвищим середнім балом з певного предмета.
def query_2(subject_id: int):
    student_avg_for_subject = session.query(
        Student.name,
        func.round(func.avg(Grade.grades), 2).label("avg_grade"),
        Subject.subject_name
    ).select_from(Grade).join(Student).join(Subject).filter(
        Subject.id == subject_id
    ).group_by(
        Subject.id,
        Student.id
    ).order_by(
        desc("avg_grade")
    ).first()

    temp_list = []
    for el in student_avg_for_subject:
        temp_list.append(str(el))
    print(f'По предмету {temp_list[2]} найвищій середній бал {temp_list[1]} має {temp_list[0]}')


# Знайти середній бал у групах з певного предмета.
def query_3(subject_id: int):
    avg_grade_in_groups_for_subject = session.query(
        Team.team_name,
        func.round(func.avg(Grade.grades), 2).label("avg_grade"),
        Subject.subject_name
    ).select_from(Grade).join(Student).join(Team).join(Subject).filter(
        Subject.id == subject_id
    ).group_by(
        Team.id,
        Subject.id
    ).order_by(
        Team.id).all()
    print(f'Середній бал в групах за предметом')
    for el in avg_grade_in_groups_for_subject:
        print(el)


# Знайти середній бал на потоці (по всій таблиці оцінок).
def query_4():
    averange = session.query(
        func.round(func.avg(Grade.grades), 2).label('avg_grade')
    ).select_from(Grade).one()
    print(f'Середній бал на потоці:{averange}')


# Знайти які курси читає певний викладач.
def query_5(teacher_id: int):
    teacher_subject = session.query(
        Teacher.name,
        Subject.subject_name,
    ).select_from(Subject).join(Teacher).filter(Teacher.id == teacher_id).all()

    all_subjects = []
    name_student = ''
    for tuples in teacher_subject:
        name_student = tuples[0]
        all_subjects.append(tuples[1])
    print({name_student: all_subjects})


# Знайти список студентів у певній групі.
def query_6(group_id: int):
    students_in_groups = session.query(
        Student.name,
        Team.team_name
    ).select_from(Student).join(Team).filter(Team.id == group_id).all()

    student_list = []
    group_name = ''
    for tuples in students_in_groups:
        student_list.append(tuples[0])
        group_name = tuples[1]
    print({group_name: student_list})


# Знайти оцінки студентів у окремій групі з певного предмета.
def query_7(subject_id: int, group_id: int):
    grades_for_subject_in_group = session.query(
        Grade.grades,
        Subject.subject_name,
        Team.team_name
    ).select_from(Grade).join(Subject).join(Student).join(Team).filter(and_(
        Subject.id == subject_id,
        Team.id == group_id
    )).all()

    all_grades = []
    group = ''
    subject = ''
    for tuples in grades_for_subject_in_group:
        all_grades.append(tuples[0])
        subject = tuples[1]
        group = tuples[2]
    print(f'Всі оцінки в групі {group} за предмет {subject}: {all_grades}')


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def query_8(teacher_id: int):
    average_for_teacher = session.query(
        func.round(func.avg(Grade.grades), 2).label('avg_grade'),
        Teacher.name
    ).select_from(Grade).join(Subject).join(Teacher).group_by(Teacher.name).filter(
        Subject.teacher_id == teacher_id
    ).all()

    avg_grade = ''
    teacher = ''
    for tuples in average_for_teacher:
        avg_grade = tuples[0]
        teacher = tuples[1]
    print(f'Середній бал у викладача {teacher}: {avg_grade}')


# Знайти список курсів, які відвідує певний студент.
def query_9(student_id: int):
    student_courses = session.query(
        Student.name,
        Subject.subject_name
    ).select_from(Student).join(Grade).join(Subject).filter(
        Student.id == student_id
    ).all()

    student = ''
    all_subjects = []
    for tuples in student_courses:
        student = tuples[0]
        all_subjects.append(tuples[1])
    print(f'Всі предмети, на які ходить {student}: {set(all_subjects)}')


# Список курсів, які певному студенту читає певний викладач.
def query_10(teacher_id: int, student_id: int):
    courses_for_student_from_teacher = session.query(
        Student.name,
        Subject.subject_name,
        Teacher.name
    ).select_from(Student).join(Grade).join(Subject).join(Teacher).filter(and_(
        Student.id == student_id,
        Teacher.id == teacher_id
    )).all()

    all_subject = []
    student = ''
    teacher = ''
    for tuples in courses_for_student_from_teacher:
        student = tuples[0]
        all_subject.append(tuples[1])
        teacher = tuples[2]
    print(f'Викладач {teacher} читає студенту {student} такі предмети: {set(all_subject)}')


# Середній бал, який певний викладач ставить певному студентові.
def query_11(student_id: int, teacher_id: int):
    avg_from_teacher_to_student = session.query(
        Student.name,
        func.round(func.avg(Grade.grades), 2).label("avg_grade"),
        Teacher.name
    ).select_from(Grade).join(Student).join(Subject).join(Teacher).filter(and_(
        Student.id == student_id,
        Teacher.id == teacher_id
    )).group_by(
        Student.id,
        Teacher.id).all()

    temp_list = []
    for el in avg_from_teacher_to_student:
        for item in el:
            temp_list.append(item)
    print(f'Від викладача {temp_list[2]} студент {temp_list[0]} отримує середній бал {temp_list[1]}')


# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def query_12(team_id: int, subject_id: int):
    last_date = session.query(
        Grade.lesson_date.label('t')
    ).select_from(Grade).join(Student).join(Team).join(Subject).order_by((desc('t'))).filter(and_(
        Team.id == team_id,
        Subject.id == subject_id
    )).first()

    grades_for_groups_in_date = session.query(
        Team.team_name,
        Grade.grades,
        Subject.subject_name,
        Grade.lesson_date.label('time')
    ).select_from(Team).join(Student).join(Grade).join(Subject).order_by(
        desc(Grade.lesson_date)).filter(and_(
            Team.id == team_id,
            Subject.id == subject_id,
        )).all()

    last_day_notes = []
    for el in grades_for_groups_in_date:
        day_edit = datetime.date(el[3]).strftime('%Y%m%d')
        for day in last_date:
            last_lesson = datetime.date(day).strftime('%Y%m%d')
            if day_edit == last_lesson:
                last_day_notes.append(el)

    team = ''
    grades = []
    subject = ''
    date = ''

    tuple_to_list = []
    for el in last_day_notes:
        tuple_to_list.append([i for i in el])

    for item in tuple_to_list:
        team = item[0]
        grades.append(item[1])
        subject = item[2]
        date = item[3]

    print(f'На останньому занятті {datetime.date(date)} з предмету {subject} група {team} отримала оцінки:{grades}')


if __name__ == '__main__':
    # query_1()
    # query_2(7)
    # query_3(5)
    # query_4()
    # query_5(2)
    # query_6(2)
    # query_7(2, 3)
    # query_8(4)
    # query_9(33)
    # query_10(3, 23)
    # query_11(34, 2)
    query_12(3, 7)
