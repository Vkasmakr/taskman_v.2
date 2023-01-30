from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employee/', views.employee, name='employee'),
    path('tasks/', views.TaskListView.as_view(), name='tasks_name'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('alltasks/', views.AllTaskListView.as_view(), name='all_tasks'),
    path('alltasksc/', views.AllTaskCListView.as_view(), name='all_tasks_c'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('projects/', views.ProjectListView.as_view(), name='all_projects'),
    path('projectsc/', views.ProjectCListView.as_view(), name='all_projects_c'),
    path('projects/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/', views.project_done, name='view-project'),
    path('alltasks/new', views.TaskInstanceCreateView.as_view(), name='task-new'),
    path('projects/new', views.ProjectCreateView.as_view(), name='project-new')
]