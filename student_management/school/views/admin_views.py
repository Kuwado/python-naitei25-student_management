from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.timezone import now


from school.models import Student, Teacher, Class, ClassStudent, ClassTeacher, Semester

from school.forms import (
    StudentForm,
    TeacherForm,
    ClassForm,
    ClassStudentForm,
    ClassTeacherForm,
)
from school.constants import Role


# Manage Students
def manage_students(request):
    students = Student.objects.all()
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("manage_students")
    else:
        form = StudentForm()
    return render(
        request, "admin_app/manage_students.html", {"students": students, "form": form}
    )


# Edit Student
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("manage_students")
    else:
        form = StudentForm(instance=student)
    return render(request, "admin_app/edit_student.html", {"form": form})


# Delete Student
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    current_date = now().date()
    semester = Semester.objects.filter(
        start_date__lte=current_date, end_date__gte=current_date
    ).first()

    is_enrolled = ClassStudent.objects.filter(
        student=student, semester__id=semester.id
    ).exists()

    if is_enrolled:
        messages.error(
            request, "Không thể xóa học sinh vì đang tham gia lớp học trong học kỳ này."
        )
        return redirect("manage_students")

    student.delete()
    messages.success(request, "Xóa học sinh thành công.")
    return redirect("manage_students")


# Manage Teachers
def manage_teachers(request):
    teachers = Teacher.objects.all()
    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("manage_teachers")
    else:
        form = TeacherForm()
    return render(
        request, "admin_app/manage_teachers.html", {"teachers": teachers, "form": form}
    )


# Edit Teacher
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("manage_teachers")
    else:
        form = TeacherForm(instance=teacher)
    return render(request, "admin_app/edit_teacher.html", {"form": form})


# Delete Teacher
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    current_date = now().date()
    semester = Semester.objects.filter(
        start_date__lte=current_date, end_date__gte=current_date
    ).first()

    is_enrolled = ClassTeacher.objects.filter(
        teacher=teacher, semester__id=semester.id
    ).exists()

    if is_enrolled:
        messages.error(
            request,
            "Không thể xóa giáo viên vì đang tham gia lớp học trong học kỳ này.",
        )
        return redirect("manage_teachers")

    teacher.delete()
    messages.success(request, "Xóa giáo viên thành công.")
    return redirect("manage_teachers")


# Manage Classes
def manage_classes(request):
    if request.user.teacher.role == Role.ADMIN.value:
        classes = Class.objects.all()
    else:
        teacher = Teacher.objects.get(username=request.user.username)
        class_ids = ClassTeacher.objects.filter(teacher=teacher).values_list(
            "classroom_id", flat=True
        )
        classes = Class.objects.filter(id__in=class_ids)

    if not classes:
        return HttpResponseForbidden(
            "You do not have permission to manage any classes."
        )

    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_classes")
    else:
        form = ClassForm()
    return render(
        request, "admin_app/manage_classes.html", {"classes": classes, "form": form}
    )


# Manage Class for Students
def manage_class_students(request):
    class_students = ClassStudent.objects.all()
    if request.method == "POST":
        form = ClassStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_class_students")
    else:
        form = ClassStudentForm()
    return render(
        request,
        "admin_app/manage_class_students.html",
        {"class_students": class_students, "form": form},
    )


# Manage Class for Teachers
def manage_class_teachers(request):
    if request.user.teacher.role != Role.ADMIN.value:
        return HttpResponseForbidden("Only admins can assign teachers to classes.")

    if request.method == "POST":
        form = ClassTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_class_teachers")
    else:
        form = ClassTeacherForm()
    return render(request, "admin_app/manage_class_teachers.html", {"form": form})
