from django.views.generic import ListView, DetailView
from rest_framework.generics import RetrieveAPIView
from .utils import *
from .models import *
from .models import Skills as Superskills
from rest_framework import generics
from .serializers import *

menu = [{'url': 'skills'}, {'url': 'projects'}]


class Home(DataMixin, ListView):
    """
    Выводим
    """
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
        'id_category').select_related('id_view').order_by('p_sorting', '-id').filter(p_status=True)
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
        return Project.objects.filter(pk=self.kwargs['pk']).prefetch_related('skills').prefetch_related(
            'id_teamlist').select_related(
            'id_category').select_related('id_view')
