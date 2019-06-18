from User.models import User, Student, Staff
from Department.models import Department, Batch, Degree
from Elective.models import OpenElective, DepartmentElective
from Subject.models import Subject, OpenElectiveSubject, DepartmentElectiveSubject
from Application.models import OpenElectiveApplication, DepartmentElectiveApplication
from datetime import date


def initialize():
    apps = OpenElectiveApplication.objects.all()
    for app in apps: app.delete()
    apps = DepartmentElectiveApplication.objects.all()
    for app in apps: app.delete()

    subs = OpenElectiveSubject.objects.all()
    for sub in subs: sub.delete()
    subs = DepartmentElectiveSubject.objects.all()
    for sub in subs: sub.delete()

    es = OpenElective.objects.all()
    for e in es: e.delete()
    es = DepartmentElective.objects.all()
    for e in es: e.delete()

    studs = Student.objects.all()
    for stud in studs: stud.delete()
    staffs = Staff.objects.all()
    for staff in staffs: staff.delete()
    users = User.objects.all()
    for user in users: user.delete()

    subs = Subject.objects.all()
    for sub in subs: sub.delete()

    bs = Batch.objects.all()
    for b in bs: b.delete()
    ds = Degree.objects.all()
    for d in ds: d.delete()
    ds = Department.objects.all()
    for d in ds: d.delete()

    cse = Department.objects.create(name="CSE")
    ece = Department.objects.create(name="ECE")
    ee = Department.objects.create(name="Electrical")
    dual = Degree.objects.create(name="Dual Degree")
    btech = Degree.objects.create(name="B. Tech.")
    batch1 = Batch.objects.create(degree=dual, year=2016)
    batch2 = Batch.objects.create(degree=btech, year=2016)

    su = User.objects.create_superuser(
        name="admin",
        email="cs16mi506@nith.ac.in",
        password="nith.123"
    )
    staff = Staff.objects.create(
        name="staff",
        email="mnprtpsingh@gmail.com",
        department=cse
    )
    staff.set_password('nith.123')
    staff.save()
    student24 = Student.objects.create(
        roll_number="16mi524",
        name="Kartik Saxene",
        email="cs16mi524@nith.ac.in",
        batch=batch1,
        department=cse
    )
    student24.set_password('nith.123')
    student24.save()
    student57 = Student.objects.create(
        roll_number="16mi557",
        name="Akash Soni",
        email="cs16mi557@nith.ac.in",
        batch=batch1,
        department=cse
    )
    student57.set_password('nith.123')
    student57.save()
    student406 = Student.objects.create(
        roll_number="16mi406",
        name="Prachi Bhore",
        email="cs16mi406@nith.ac.in",
        batch=batch2,
        department=ece
    )
    student406.set_password('nith.123')
    student406.save()
    student247 = Student.objects.create(
        roll_number="16247",
        name="Piyush Jain",
        email="cs16mi247@nith.ac.in",
        batch=batch2,
        department=ee
    )
    student247.set_password('nith.123')
    student247.save()

    oe = OpenElective.objects.create(
        number_of_courses=1,
        starts=date(2019, 6, 20),
        ends=date(2019, 6, 30)
    )
    oe.batches.add(batch1, batch2)
    de = DepartmentElective.objects.create(
        number_of_courses=1,
        starts=date(2019, 6, 24),
        ends=date(2019, 6, 30),
        department=cse
    )
    de.batches.add(batch1, batch2)
    oe2 = OpenElective.objects.create(
        number_of_courses=1,
        starts=date(2019, 6, 30),
        ends=date(2019, 7, 10)
    )
    oe2.batches.add(batch2)

    ds = Subject.objects.create(subject_name="Data Structures")
    cg = Subject.objects.create(subject_name="Computer Graphics")
    ai = Subject.objects.create(subject_name="Artificial Intelligence")
    nn = Subject.objects.create(subject_name="Neural Networks")
    ws = Subject.objects.create(subject_name="Wireless Sensor Design")
    oes1 = OpenElectiveSubject.objects.create(
        course_code="CSD-315",
        subject=ds,
        minimum_seats=30,
        maximum_seats=100,
        elective=oe,
        department=cse
    )
    oes2 = OpenElectiveSubject.objects.create(
        course_code="CSD-315(b)",
        subject=cg,
        minimum_seats=30,
        maximum_seats=100,
        elective=oe,
        department=cse
    )
    oes3 = OpenElectiveSubject.objects.create(
        course_code="EEO-315",
        subject=nn,
        minimum_seats=30,
        maximum_seats=100,
        elective=oe,
        department=ee
    )
    oes4 = OpenElectiveSubject.objects.create(
        course_code="ECE-314",
        subject=ws,
        minimum_seats=30,
        maximum_seats=100,
        elective=oe,
        department=ece
    )
    oes5 = OpenElectiveSubject.objects.create(
        course_code="CSD-315",
        subject=ds,
        minimum_seats=30,
        maximum_seats=100,
        elective=oe2,
        department=cse
    )
    oes6 = OpenElectiveSubject.objects.create(
        course_code="EEO-315",
        subject=nn,
        minimum_seats=30,
        maximum_seats=100,
        elective=oe2,
        department=ee
    )
    oes7 = OpenElectiveSubject.objects.create(
        course_code="ECE-314",
        subject=ws,
        minimum_seats=30,
        maximum_seats=100,
        elective=oe2,
        department=ece
    )
    des1 = DepartmentElectiveSubject.objects.create(
        course_code="CSD-315",
        subject=cg,
        minimum_seats=30,
        maximum_seats=100,
        elective=de
    )
    des2 = DepartmentElectiveSubject.objects.create(
        course_code="CSD-315(b)",
        subject=ai,
        minimum_seats=30,
        maximum_seats=100,
        elective=de
    )

    student24.subjects.add(ai)

    # oea1 = OpenElectiveApplication.objects.create(
    #     student=student24,
    #     cgpa=8.0,
    #     elective=oe
    # )
    # oea2 = OpenElectiveApplication.objects.create(
    #     student=student57,
    #     cgpa=8.5,
    #     elective=oe
    # )
    # dea1 = DepartmentElectiveApplication.objects.create(
    #     student=student24,
    #     cgpa=8.0,
    #     elective=de
    # )
    # dea2 = DepartmentElectiveApplication.objects.create(
    #     student=student57,
    #     cgpa=8.5,
    #     elective=de
    # )