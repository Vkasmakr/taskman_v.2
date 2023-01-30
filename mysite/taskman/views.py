from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Employee, TaskInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin, CreateView
from .forms import TaskCommentForm, ProjectCommentForm, TaskCreateForm, ProjectCreateForm
from django.shortcuts import get_object_or_404


# Create your views here.
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
        return TaskInstance.objects.filter(assign_employees__user=self.request.user).filter(project_id__completed_on=False)\
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
        task_list = TaskInstance.objects.filter(project_id__group_id__id=current_employee.group_id.id).filter\
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
        task_list = TaskInstance.objects.filter(project_id__group_id__id=current_employee.group_id.id)\
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
    # fields = ('project_id', 'job_title', 'description', 'enddate', 'assign_employees')
    success_url = '/taskman/alltasks/'
    template_name = 'task_create_form.html'
    form_class = TaskCreateForm

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
        return super().form_valid(form)


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


# Cia yra funkcija, kuri isfilturoja atitinkamo projecto completed_on lauka ir ja suvykdzius, pakeicia statusa i True
def project_done(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.completed_on = True
        project.save()
        return redirect('view-project', id=pk)

    return render(request, 'project_detail.html', {'project': project})


# Employee profile:
@login_required
def employee(request):
    return render(request, "employee.html")
