from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Employee, TaskInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from .forms import TaskCommentForm, ProjectCommentForm, TaskCreateForm, ProjectCreateForm, TaskUpdateForm
from datetime import datetime
from django.shortcuts import get_object_or_404


# Create your views here.
class MyTeamListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    paginate_by = 5
    template_name = 'my_team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        # Thanks chat GPT
        employee_list = self.get_queryset()
        for employee in employee_list:
            tasks = TaskInstance.objects.filter(assign_employees=employee)
            overdue_tasks = tasks.filter(enddate__lt=datetime.now(), completed_on=False)
            employee.overdue_task_count = overdue_tasks.count()
        context['employee_list'] = employee_list
        return context

    def get_queryset(self):
        current_employee = Employee.objects.get(user=self.request.user)
        return Employee.objects.filter(group_id=current_employee.group_id)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = TaskInstance
    paginate_by = 5
    template_name = 'my_task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        context['has_assigned_tasks'] = self.get_queryset().filter(assign_employees__user=self.request.user).exists()
        return context

    def get_queryset(self):
        return TaskInstance.objects.filter(assign_employees__user=self.request.user).filter(
            project_id__completed_on=False) \
            .filter(completed_on=False)


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5
    template_name = 'project_list.html'

    def get_queryset(self):
        current_employee = Employee.objects.get(user=self.request.user)
        task_list = Project.objects.filter(group_id__id=current_employee.group_id.id).filter(completed_on=False)
        return task_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context


class ProjectCListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5
    template_name = 'project_list_completed.html'

    def get_queryset(self):
        current_employee = Employee.objects.get(user=self.request.user)
        task_list = Project.objects.filter(group_id__id=current_employee.group_id.id).filter(completed_on=True)
        return task_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context


class TaskDetailView(FormMixin, generic.DetailView, LoginRequiredMixin):
    model = TaskInstance  # automatiskai sukuriamas kintamasis Book -> book
    template_name = 'task_detail.html'  # nurodome is kur ims apipavidalinima internete
    form_class = TaskCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context

    def get_object(self):
        return TaskInstance.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.task = self.object
        form.instance.user = self.request.user
        form.save()
        return super(TaskDetailView, self).form_valid(form)


class AllTaskListView(LoginRequiredMixin, generic.ListView):
    model = TaskInstance
    paginate_by = 5
    template_name = 'all_tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context

    def get_queryset(self):
        current_employee = Employee.objects.get(user=self.request.user)
        task_list = TaskInstance.objects.filter(project_id__group_id__id=current_employee.group_id.id).filter \
            (project_id__completed_on=False).filter(completed_on=False)
        return task_list


class AllTaskCListView(LoginRequiredMixin, generic.ListView):
    model = TaskInstance
    paginate_by = 5
    template_name = 'all_tasks_completed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context

    def get_queryset(self):
        current_employee = Employee.objects.get(user=self.request.user)
        task_list = TaskInstance.objects.filter(project_id__group_id__id=current_employee.group_id.id) \
            .filter(completed_on=True)
        return task_list


class ProjectDetailView(FormMixin, generic.DetailView, LoginRequiredMixin):
    model = Project  # automatiskai sukuriamas kintamasis Book -> book
    template_name = 'project_detail.html'  # nurodome is kur ims apipavidalinima internete
    form_class = ProjectCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context

    def get_object(self):
        return Project.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.project = self.object
        form.instance.user = self.request.user
        form.save()
        return super(ProjectDetailView, self).form_valid(form)


class TaskInstanceCreateView(LoginRequiredMixin, CreateView):
    model = TaskInstance
    success_url = '/taskman/alltasks/'
    template_name = 'task_create_form.html'
    form_class = TaskCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context

    def form_valid(self, form):
        assign_employee = form.cleaned_data['assign_employees']  # gets the employee from list
        form.instance.assign_employees = assign_employee
        project = form.cleaned_data['project_id']
        group = project.group_id
        form.fields['assign_employees'].queryset = Employee.objects.filter(group_id__id=group.id)
        response = super().form_valid(form)
        self.object.assign_employees.task_number += 1
        self.object.assign_employees.save()
        return response

    # def form_valid(self, form):
    #     form.instance.assign_employees = Employee.objects.get(user=self.request.user)
    #     project = form.cleaned_data['project_id']
    #     group = project.group_id
    #     form.fields['assign_employees'].queryset = Employee.objects.filter(group_id__id=group.id)
    #     response = super().form_valid(form)
    #     self.object.assign_employees.task_number += 1
    #     self.object.assign_employees.save()
    #     return response


class TaskInstanceUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskInstance
    success_url = '/taskman/alltasks/'
    template_name = 'task_create_form.html'
    form_class = TaskUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context

    def form_valid(self, form):
        form.instance.assign_employees = Employee.objects.get(user=self.request.user)
        project = form.cleaned_data['project_id']
        group = project.group_id
        form.fields['assign_employees'].queryset = Employee.objects.filter(group_id__id=group.id)

        previous_employee = self.get_object().assign_employees
        new_employee = form.cleaned_data['assign_employees']

        if previous_employee != new_employee:
            previous_employee.task_number -= 1
            previous_employee.save()
            new_employee.task_number += 1
            new_employee.save()

        return super().form_valid(form)


class TaskInstanceDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskInstance
    success_url = "/taskman/alltasks/"
    template_name = 'task_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context

    def delete(self, request, *args, **kwargs):
        task_instance = self.get_object()
        assigned_employee = task_instance.assign_employees
        assigned_employee.task_number -= 1
        assigned_employee.save()
        return super().delete(request, *args, **kwargs)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    success_url = '/taskman/projects/'
    template_name = 'project_create_form.html'
    form_class = ProjectCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = Employee.objects.get(user=self.request.user)
        context['current_employee'] = current_employee
        return context

    def form_valid(self, form):
        form.instance.assign_employees = Employee.objects.get(user=self.request.user)
        return super().form_valid(form)


def index(request):
    if request.user.is_authenticated:
        current_employee = Employee.objects.get(user=request.user)
        context = {'current_employee': current_employee}
    else:
        context = {}
    return render(request, 'index.html', context=context)


def project_done(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.completed_on = True
        project.save()
        return redirect('project-detail', pk=pk)

    return render(request, 'project_detail.html', {'project': project})


def project_open(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.completed_on = False
        project.save()
        return redirect('project-detail', pk=pk)

    return render(request, 'project_detail.html', {'project': project})


def task_done(request, pk):
    task = TaskInstance.objects.get(id=pk)
    if request.method == 'POST':
        task.completed_on = True
        task.assign_employees.task_number = task.assign_employees.task_number - 1
        task.assign_employees.save()
        task.save()
        return redirect('task-detail', pk=pk)

    return render(request, 'task_detail.html', {'task': task})


def task_open(request, pk):
    task = TaskInstance.objects.get(id=pk)
    if request.method == 'POST':
        task.completed_on = False
        task.assign_employees.task_number = task.assign_employees.task_number + 1
        task.assign_employees.save()
        task.save()
        return redirect('task-detail', pk=pk)

    return render(request, 'task_detail.html', {'task': task})


# Employee profile:
@login_required
def employee(request):
    return render(request, "employee.html")
