from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from rest_framework.generics import RetrieveAPIView, ListAPIView

from .utils import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Skills as Superskills
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

    def get_queryset(self):
        return Project.objects.all().select_related('id_category').prefetch_related('skills').select_related(
            'id_view').prefetch_related('id_teamlist')


# def skill(request, skill_slug):
#     skill = Superskills.objects.get(slug=skill_slug)
#     skill_sl = skill.slug
#     projects = Project.objects.filter(skills__slug=skill_sl)
#     return render(request, 'skill.html', {'skill': skill, 'projects': projects})


class Skill(DataMixin, DetailView):
    model = Superskills
    context_object_name = 'skill'
    template_name = 'skill.html'
    slug_url_kwarg = 'skill_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        c_def = self.get_user_context(title=context['skill'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


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
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Superskills.objects.all().prefetch_related('project')


# def project(request, pk):
#     project = Project.objects.get(pk=pk)
#     print(project.p_name)
#     return render(request, 'project.html', {'project': project})


class ProjectDetail(DataMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'project.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        c_def = self.get_user_context(title=context['project'].p_name)
        print(context['object'].p_name)
        context = dict(list(context.items()) + list(c_def.items()))
        print(context)
        return context


class ProjectList(generics.ListCreateAPIView):
    """
    Выводим список проектов
    """
    queryset = Project.objects.all().prefetch_related('skills').prefetch_related('id_teamlist').select_related(
        'id_category').select_related('id_view').order_by('p_sorting','-id').filter(p_status=True)
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()


class CategoryList(generics.ListCreateAPIView):
    """
    Выводим список проектов
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save()


class CatSkiList(generics.ListCreateAPIView):
    """
    Выводим список проектов
    """
    queryset = CatSkill.objects.all().prefetch_related('skills').order_by('cs_sorting')
    serializer_class = CatSkillSerializer

    def perform_create(self, serializer):
        serializer.save()


class ProjectDetailed(RetrieveAPIView):
    """
    Выводим проект детально
    """
    serializer_class = ProjectDet

    def get_queryset(self, **kwargs):
        # pro = Project.objects.get(pk=self.kwargs['pk'])
        # serializer = ProjectDet(pro)
        # return Response(serializer.data)
        return Project.objects.filter(pk=self.kwargs['pk']).prefetch_related('skills').prefetch_related('id_teamlist').select_related(
        'id_category').select_related('id_view')
