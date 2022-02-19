from rest_framework import serializers
from .models import *


class ProjectSerializer(serializers.ModelSerializer):
    png = serializers.SerializerMethodField(method_name='get_name')

    class Meta:
        model = Project
        fields = ['p_name', 'p_description', 'png', 'id_category', 'id_view', 'p_organization', 'slug', 'p_i_did',
                  'photo', 'webp_pre', 'webp_det', 'png_pre', 'png_det', 'p_link', 'skills', 'p_git', 'p_sorting',
                  'p_status']

    def get_name(self, instance):
        request = self.context.get('request')
        i = {}
        i['p_name'] = instance.p_name
        i['p_description'] = instance.p_description
        return i
