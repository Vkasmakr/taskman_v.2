from .models import TaskComment, ProjectComment, TaskInstance, Project, Employee
from django import forms
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


# This is a form for ProjectCreateView in views.py
class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'group_id', 'employee_req', 'enddate']
        widgets = {'enddate': DateInput()}


# This is a form for ProjectUpdateView in views.py
class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'group_id', 'employee_req', 'enddate']
        widgets = {'enddate': DateInput()}


# This is a form for TaskInstanceCreateView in views.py
class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = TaskInstance
        fields = ['project_id', 'job_title', 'description', 'enddate', 'assign_employees']
        widgets = {'enddate': DateInput()}


# This is a form for TaskInstanceUpdateView in views.py
class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskInstance
        fields = ['project_id', 'job_title', 'description', 'enddate', 'assign_employees']
        widgets = {'enddate': DateInput()}


# This is a comment form for TaskDetailView in views.py
class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content', 'task', 'user')
        widgets = {'task': forms.HiddenInput(), 'user': forms.HiddenInput()}


# This is a comment form for ProjectDetailView in views.py
class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ('content', 'project', 'user')
        widgets = {'project': forms.HiddenInput(), 'user': forms.HiddenInput()}


# This is a form for employee functions in views.py, used for User class change
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


# This is a form for employee functions in views.py, used for Employee class change
class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['photo']