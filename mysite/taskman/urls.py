from django.urls import path, include
from . import views

urlpatterns = [
    # general links to top pages of base.html
    path('', views.index, name='index'),
    path('employee/', views.employee, name='employee-page'),
    path('myteam/', views.MyTeamListView.as_view(), name='my-team'),

    # links to task management and view pages
    path('tasks/', views.TaskListView.as_view(), name='tasks_name'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('alltasks/', views.AllTaskListView.as_view(), name='all_tasks'),
    path('alltasksc/', views.AllTaskCListView.as_view(), name='all_tasks_c'),
    path('alltasks/<int:pk>/done', views.task_done, name='complete-task'),
    path('alltasks/<int:pk>/open', views.task_open, name='open-task'),


    path('alltasks/new', views.TaskInstanceCreateView.as_view(), name='task-new'),
    path('alltasks/<int:pk>/update', views.TaskInstanceUpdateView.as_view(), name='task-update'),
    path('alltasks/<int:pk>/delete', views.TaskInstanceDeleteView.as_view(), name='delete-task'),

    # general link to login/logout pages
    path('accounts/', include('django.contrib.auth.urls')),

    # links to project management and view pages
    path('projects/', views.ProjectListView.as_view(), name='all_projects'),
    path('projectsc/', views.ProjectCListView.as_view(), name='all_projects_c'),
    path('projects/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/done', views.project_done, name='complete-project'),
    path('projects/<int:pk>/open', views.project_open, name='open-project'),

    path('projects/new', views.ProjectCreateView.as_view(), name='project-new'),
    path('projects/<int:pk>/update', views.ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete', views.ProjectDeleteView.as_view(), name='project-delete'),
]