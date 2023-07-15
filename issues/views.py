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
from .models import Issue, Status, Priority
from django.urls import reverse_lazy

class IssueListView(ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issue_list"] = Issue.objects.all()#i need to add a sort with de priority
        return context


class IssueDetailView(DetailView):
    template_name = "issues/detail.html"
    model = Issue


class IssueCreateView(LoginRequiredMixin, CreateView, UserPassesTestMixin):
    template_name = "issues/new.html"
    model = Issue
    fields = ['summary', 'description', 'status', 'priority', 'assignee']

    # def form_valid(self, form):
    #     form.instance.reporter = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        po = Role.objects.get(name = "product owner")
        return super().request.user.role == po


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ['summary', 'description', 'status', 'priority', 'assignee']

    def test_func(self):
        issue_obj = self.get_object()
        return issue_obj.reporter == self.request.user


class  IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue

    def test_func(self):
        po = Role.objects.get(name= "product owner")
        done_status = Status.objects.get(name = "done")
        issue = self.get_object()
        if issue.status == done_status and self.request.user.role == po:
            return True
        return False
