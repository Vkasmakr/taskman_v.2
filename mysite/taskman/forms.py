from .models import TaskComment, ProjectComment, TaskInstance, Project, Employee
from django import forms
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'group_id', 'employee_req', 'enddate']
        widgets = {'enddate': DateInput()}


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'group_id', 'employee_req', 'enddate']
        widgets = {'enddate': DateInput()}


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = TaskInstance
        fields = ['project_id', 'job_title', 'description', 'enddate', 'assign_employees']
        widgets = {'enddate': DateInput()}


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskInstance
        fields = ['project_id', 'job_title', 'description', 'enddate', 'assign_employees']
        widgets = {'enddate': DateInput()}


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content', 'task', 'user')
        widgets = {'task': forms.HiddenInput(), 'user': forms.HiddenInput()}


class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ('content', 'project', 'user')
        widgets = {'project': forms.HiddenInput(), 'user': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['photo']