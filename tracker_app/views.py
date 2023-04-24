from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from .models import ProjectList, BugItem
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.

class UserLoginView(LoginView):
    template_name = "tracker_app/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")


class UserRegisterView(FormView):
    template_name = "tracker_app/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegisterView, self). form_valid(form)


class ProjectListView(LoginRequiredMixin, ListView):
    model = ProjectList
    template_name = "tracker_app/index.html"
    context_object_name = 'title'

    # def get_queryset(self):
    #     return ProjectList.objects.filter(user=self.request.user)

class BugListView(LoginRequiredMixin, ListView):
    model = BugItem
    template_name = "tracker_app/bug_list.html"

    def get_queryset(self):
        return BugItem.objects.filter(project_id=self.kwargs["project_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["project"] = ProjectList.objects.get(id=self.kwargs["project_id"])
        return context


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = ProjectList
    fields = ["title"]

    def get_context_data(self, **kwargs):
        context = super(ProjectCreate, self).get_context_data()
        context["title"] = "Add a new project"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class BugCreate(LoginRequiredMixin, CreateView):
    model = BugItem
    fields = [
        "title",
        "description",
        "urgency",
        "completed",
        "assignee"
    ]

    def get_initial(self):
        initial_data = super(BugCreate, self).get_initial()
        project = ProjectList.objects.get(id=self.kwargs["project_id"])
        initial_data["project_list"] = project
        return initial_data


    def get_context_data(self, **kwargs):
        context = super(BugCreate, self).get_context_data()
        project = ProjectList.objects.get(id=self.kwargs["project_id"])
        context["project"] = project
        context["title"] = "Create a new item"
        return context

    def form_valid(self, form):
        form.instance.project = ProjectList.objects.get(id=self.kwargs["project_id"])
        form.instance.reporter = self.request.user
        return super(BugCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("project", args=[self.object.project_id])


class BugUpdate(LoginRequiredMixin, UpdateView):
    model = BugItem
    fields = [
        "title",
        "description",
        "urgency",
        "completed"
    ]

    def get_context_data(self, **kwargs):
        context = super(BugUpdate, self).get_context_data()
        context["project"] = self.object.project
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("project", args=[self.object.project_id])


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = ProjectList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")


class BugDelete(LoginRequiredMixin, DeleteView):
    model = BugItem

    def get_success_url(self):
        return reverse_lazy("project", args=[self.kwargs["project_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.object.project
        return context

class BugDetailView(LoginRequiredMixin, DetailView):
    model = BugItem
    template_name = "tracker_app/bug_view.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

class AssignedBugListView(LoginRequiredMixin, ListView):
    model = BugItem
    template_name = "tracker_app/assignedbug_list.html"

    def get_queryset(self):
        return BugItem.objects.filter(assignee=self.request.user)

    def get_context_data(self):
        context = super().get_context_data()
        #context["project"] = BugItem.objects.get(id=self.kwargs["project_id"])
        return context
