from django.db import models
from django.contrib.auth.models import Group, User
from PIL import Image
from django.urls import reverse
from django.core.validators import MinValueValidator
from datetime import date


# A model for Project
class Project(models.Model):
    title = models.CharField('Project title', max_length=100, help_text='Enter project title')
    description = models.TextField('Description', max_length=2000, help_text='Enter project description')
    group_id = models.ForeignKey(Group, help_text='Assign to a team', blank=True, on_delete=models.SET_NULL, null=True)
    employee_req = models.IntegerField('Number of employees expected. Min:1', default=0, validators=[MinValueValidator(1)])
    enddate = models.DateTimeField('Requested finish date', null=True, blank=True)
    created_on = models.DateTimeField(editable=False, auto_now_add=True)
    updated_on = models.DateTimeField(editable=False, auto_now_add=True)
    completed_on = models.BooleanField('Completed', default=False)

    def __str__(self):
        return self.title

    def absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])


# A model for team roles. This will be used to determine what pages each user can access
class TeamRole(models.Model):
    name = models.CharField('Role in a team', max_length=200, help_text='Enter Team role')

    def __str__(self):
        return self.name


# A model for Employee
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, help_text='Assign to a team', on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(default='default.png', upload_to='profile_pics')
    team_role = models.ForeignKey(TeamRole, help_text='Assign a position', on_delete=models.SET_NULL, null=True, blank=True)
    # Task number - skirtas skaiciuoti kiek uzduociu dabartiniu metu yra priskirta konkreciam Employee
    task_number = models.IntegerField('Number of tasks assigned', default=0)

    def __str__(self):
        return f"Username: {self.user.username}\n / Team: {self.group_id.name} \n / Position: {self.team_role.name}"

    # to adjust he size of uploaded profile pictures
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)


# Task Instance to assign employess for specific task:
class TaskInstance(models.Model):
    project_id = models.ForeignKey('Project', help_text='Assign to a task', on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField('Task title', max_length=200, help_text='Enter Task role', null=True, blank=True)
    description = models.TextField('Description', max_length=2000, help_text='Enter task description', null=True, blank=True)
    enddate = models.DateTimeField('Requested finish date', null=True, blank=True)
    completed_on = models.BooleanField('Completed', default=False)
    # Nukreipia i konkretu Employee
    assign_employees = models.ForeignKey(Employee, help_text='Select employees to task', on_delete=models.CASCADE)

    def __str__(self):
        return self.project_id.title

    def absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])

    # checking if task deadline are not overdue
    @property
    def is_overdue(self):
        if self.enddate and date.today() > self.enddate:
            return True
        else:
            return False


# for comments in TaskInstance's detailed view
class TaskComment(models.Model):
    task = models.ForeignKey(TaskInstance, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Comment', max_length=2000)


# for comments in Project's detailed view
class ProjectComment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Comment', max_length=2000)




