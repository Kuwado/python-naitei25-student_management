from django.urls import path, include
from school.views import auth_views, teacher_view, action_views, admin_views

# Khai báo view tương ứng với url
urlpatterns = [
    path("", teacher_view.ClassListView.as_view(), name="class-list"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path(
        "class/<int:class_id>/semester/<int:semester_id>/",
        teacher_view.StudentListView.as_view(),
        name="student-list",
    ),
    path(
        "student/<int:pk>",
        teacher_view.StudentDetailView.as_view(),
        name="student-detail",
    ),
    path(
        "class/<int:class_id>/semester/<int:semester_id>/attendances",
        teacher_view.AttendancesView.as_view(),
        name="attendance-tracking",
    ),
    path(
        "attendance/tracking/",
        action_views.post_attendance,
        name="tracking",
    ),
    path(
        "class/<int:class_id>/semester/<int:semester_id>/subject/<int:subject_id>",
        teacher_view.GradeView.as_view(),
        name="grade",
    ),
    path(
        "grade/update/",
        action_views.post_grade,
        name="grade-update",
    ),
    path(
        "class/<int:class_id>/achievements/semester/<int:semester_id>",
        teacher_view.achievement_view,
        name="achievements",
    ),
    # -------------------------------------- Admin ------------------------------------------
    # Students
    path("students/", admin_views.manage_students, name="manage_students"),
    path(
        "students/edit/<int:student_id>/", admin_views.edit_student, name="edit_student"
    ),
    path(
        "students/delete/<int:student_id>/",
        admin_views.delete_student,
        name="delete_student",
    ),
    # Teachers
    path("teachers/", admin_views.manage_teachers, name="manage_teachers"),
    path(
        "teachers/edit/<int:teacher_id>/", admin_views.edit_teacher, name="edit_teacher"
    ),
    path(
        "teachers/delete/<int:teacher_id>/",
        admin_views.delete_teacher,
        name="delete_teacher",
    ),
    # Classes
    path("classes/", admin_views.manage_classes, name="manage_classes"),
    path(
        "classes/students/",
        admin_views.manage_class_students,
        name="manage_class_students",
    ),
    path(
        "classes/teachers/",
        admin_views.manage_class_teachers,
        name="manage_class_teachers",
    ),
]
