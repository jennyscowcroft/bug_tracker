from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path(
        "",
        views.ProjectListView.as_view(),
        name="index"
    ),
    path(
        "login/",
        views.UserLoginView.as_view(),
        name="login"
    ),
    path(
        "register/",
        views.UserRegisterView.as_view(),
        name="register"
    ),
    path(
        "logout/",
        views.LogoutView.as_view(next_page='login'),
        name="logout"
    ),
    path(
        "project/<int:project_id>/",
        views.BugListView.as_view(),
        name="project"
    ),
    # CRUD patterns for ToDoLists
    path(
        "project/add/",
        views.ProjectCreate.as_view(),
        name="project-add"
    ),
    path(
        "project/<int:pk>/delete/",
        views.ProjectDelete.as_view(),
        name="project-delete"
    ),
    path(
        "project/<int:project_id>/bug/add/",
        views.BugCreate.as_view(),
        name="bug-add",
    ),
    path(
        "project/<int:project_id>/bug/<int:pk>/",
        views.BugUpdate.as_view(),
        name="bug-update",
    ),
    path(
        "project/<int:project_id>/bug/<int:pk>/view",
        views.BugDetailView.as_view(),
        name="bug-detail",
    ),
    path(
        "project/<int:project_id>/bug/<int:pk>/delete/",
        views.BugDelete.as_view(),
        name="bug-delete",
    ),
    ]