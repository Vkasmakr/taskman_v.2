from django.contrib import admin
from .models import Project, Employee, TeamRole, TaskInstance
# from .models import EmployeeWork


# Register your models here.
class TaskInstanceAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'job_title', 'assign_employees', 'enddate', 'completed_on')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'enddate', 'created_on', 'updated_on', 'completed_on')
    list_filter = ('enddate', 'created_on', 'group_id', 'updated_on')
    search_fields = ('title', 'group_id__name')
    list_editable = ['enddate']


# class EmployeeWorkAdmin(admin.TabularInline):
#     model = EmployeeWork
#     list_display = ('employee', 'task_number')
#     list_editable = ['task_number']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'team_role', 'group_id', 'task_number')
    list_filter = ('team_role', 'group_id')
    list_editable = ('team_role', 'group_id')
    # inlines = [EmployeeWorkAdmin]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(TeamRole)
admin.site.register(TaskInstance, TaskInstanceAdmin)