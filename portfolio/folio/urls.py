from django.urls import path
# from . import views
from .views import *

urlpatterns = [
    # path('', views.home, name='home'),
    path('', Home.as_view(), name='home'),
    path('skill/<int:pk>', skill, name='skill'),
    path('skills', Skills.as_view(), name='skills'),
    path('project/<int:pk>',project,name='project'),
    path('projects/', ProjectList.as_view()),
]

