"""
URL configuration for Taskmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from manager.views import home,edit_task_todo, edit_task_ongo, todo_to_ongo, ongo_to_comp, todo_to_comp, deleteTask_comp, deleteTask_ongo, deleteTask_todo, ongo_todo, comp_ongo, comp_todo, login_view, register_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),
    path('edit/<int:task_id>/', edit_task_todo, name='edit_task'),
    path('edit/ongoing/<int:task_id>/', edit_task_ongo, name='edit_task_ongo'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path("todo-ongo/<int:id>/", todo_to_ongo, name='todo_ongo'),
    path("ongo-comp/<int:id>/", ongo_to_comp, name='ongo_comp'),
    path('todo-comp/<int:id>/', todo_to_comp, name='todo_comp'),
    path('delete-todo/<int:id>/',deleteTask_todo, name='delete_todo'),
    path('delete-ongo/<int:id>/',deleteTask_ongo, name='delete_ongo'),
    path('delete-comp/<int:id>/',deleteTask_comp, name='delete_comp'),
    path('ongo-todo/<int:id>/', ongo_todo, name='ongo_todo'),
    path('comp-ongo/<int:id>/', comp_ongo, name='comp_ongo'),
    path('comp-todo/<int:id>/', comp_todo, name='comp_todo'),
]
