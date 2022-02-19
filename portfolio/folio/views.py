from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from .utils import *
from .models import *
from rest_framework import generics, permissions, mixins, status
from .serializers import *

menu = [{'url': 'skills'}, {'url': 'projects'}]


# def home(request):
#     projects = Project.objects.all()
#     return render(request, 'home.html', {'projects': projects})

class Home(DataMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def skill(request, pk):
    skill = Skills.objects.get(pk=pk)
    return render(request, 'skill.html', {'skill': skill})


# def skills(request):
#     skills = Skills.objects.all()
#     return render(request, 'skills.html', {'skills': skills})

class Skills(DataMixin, ListView):
    model = Skills
    context_object_name = 'skills'
    template_name = 'skills.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Скиллы')
        context = dict(list(context.items())+list(c_def.items()))
        print(context)
        return context



def project(request, pk):
    project = Project.objects.get(pk=pk)
    print(project.p_name)
    return render(request, 'project.html', {'project': project})


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()
