from rest_framework.generics import RetrieveAPIView
from .models import *
from rest_framework import generics
from .serializers import *


class ProjectList(generics.ListCreateAPIView):
    """
    Выводим список проектов
    """
    queryset = Project.objects.all().prefetch_related('skills').prefetch_related('id_teamlist').select_related(
        'id_category').select_related('id_view').order_by('p_sorting', '-id').filter(p_status=True)
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()


class CatSkiList(generics.ListCreateAPIView):
    """
    Выводим список категорий навыков
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
