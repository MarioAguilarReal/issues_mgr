from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .models import (
    Issue,
    Status,
    Priority
)
from django.urls import reverse_lazy
from accounts.models import  (
    Role,
    Team,
    CustomUser
)
from django.core.exceptions import PermissionDenied

class IssueListView(ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issue_list"] = Issue.objects.all().order_by("priority").reverse()#i need to add a sort with de priority
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reporter_team = self.request.user.team
        po_role = Role.objects.get(name="product owner")
        to_do_status = Status.objects.get(name="to do")
        in_p_status = Status.objects.get(name="in progress")
        done_status = Status.objects.get(name="done")
        reporter = CustomUser.objects.filter(team=reporter_team).get(role=po_role)
        context["to_do_list"] = Issue.objects.filter(
            reporter=reporter).filter(status=to_do_status).order_by("priority")
        context["in_p_list"] = Issue.objects.filter(
            reporter=reporter).filter(status=in_p_status).order_by("priority")
        context["done_list"] = Issue.objects.filter(
            reporter=reporter).filter(status=done_status).order_by("priority")
        return context

class IssueDetailView(
    DetailView,
    LoginRequiredMixin,
    UserPassesTestMixin):
    template_name = "issues/detail.html"
    model = Issue

    def test_func(self):






class IssueCreateView(
    LoginRequiredMixin,
    CreateView,
    UserPassesTestMixin):
    template_name = "issues/new.html"
    model = Issue
    fields = ['summary', 'description', 'status', 'priority', 'assignee']

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

    def test_func(self):
        po = Role.objects.get(name = "product owner")
        return super().request.user.role == po

class IssueUpdateView(
    LoginRequiredMixin,
    UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ['summary', 'description', 'status', 'priority', 'assignee']

    def form_valid(self):
        issue_obj = self.get_object()
        if form.instance.status != issue.status:
            if self.request.user.role.name != "Developer":
                raise PermissionDenied()

        if form.instance.assignee != issue.assignee:
            if self.request.user.role.name != "Scrum Master":
                raise PermissionDenied()

        return super().form_valid(form)

    def test_func(self):
        team = self.get_object().reporter.team
        return self.request.user.team == team

class  IssueDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView):
    template_name = "issues/delete.html"
    model = Issue

    def test_func(self):
        po = Role.objects.get(name= "product owner")
        done_status = Status.objects.get(name = "done")
        issue = self.get_object()
        if issue.status == done_status and self.request.user.role == po:
            return True
        return False
