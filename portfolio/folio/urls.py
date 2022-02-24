from django.urls import path
# from . import views
from .views import *

urlpatterns = [
    # path('', views.home, name='home'),
    path('', Home.as_view(), name='home'),
    # path('skill/<slug:skill_slug>', skill, name='skill'),
    path('skill/<slug:skill_slug>', Skill.as_view(), name='skill'),
    path('skills', Skills.as_view(), name='skills'),
    # path('project/<int:pk>',project,name='project'),
    path('project/<slug:slug>',ProjectDetail.as_view(), name='project'),
    path('projects/', ProjectList.as_view()),
]

