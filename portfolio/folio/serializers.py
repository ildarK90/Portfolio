from django.forms import model_to_dict
from rest_framework import serializers
from .models import *
from operator import itemgetter


class CatSkillSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='cs_name')
    skill = serializers.SerializerMethodField(method_name='get_skills')

    class Meta:
        model = CatSkill
        fields = ['category', 'skill']

    def get_skills(self, instance):
        request = self.context.get('request')
        skilli = []
        for i in instance.skills.all().filter(s_status=True):
            skills = {}
            skills['id_skill'] = i.pk
            skills['s_name'] = i.s_name
            skills['s_description'] = i.s_description
            if i.s_img:
                skills['s_img'] = i.s_img.url
            else:
                skills['s_img'] = None
            skills['s_quantity'] = i.s_quantity
            skills['s_level'] = i.s_level
            skills['s_sorting'] = i.s_sorting
            skilli.append(skills)
            # skilli.sort(key=lambda x: x.id_skill)
            skilli = sorted(skilli, key=itemgetter('s_sorting'), reverse=False)
            print(skilli)

        return skilli


class ProjectSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField(method_name='get_image')
    category = serializers.CharField(source='id_category')
    id_project = serializers.CharField(source='pk')

    class Meta:
        model = Project
        fields = ['id_project', 'category', 'p_name', 'p_link', 'img']

    def get_image(self, instance):
        request = self.context.get('request')
        webp_list = []
        if type(instance.p_img_large_webp) is dict:
            for i in instance.p_img_large_webp.values():
                my_str = str(i).replace('\\', '/')
                webp_list.append(my_str)
        png_list = []
        if type(instance.p_img_large_png) is dict:
            for i in instance.p_img_large_png.values():
                my_str = str(i).replace('\\', '/')
                png_list.append(my_str)
        img = {}
        img['png'] = png_list
        img['webp'] = webp_list
        print(img)
        return img


class ProjectDet(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)
    team_link = serializers.SerializerMethodField(method_name='get_team')
    view = serializers.CharField(source='id_view')
    img = serializers.SerializerMethodField(method_name='get_image')

    class Meta:
        model = Project
        fields = ['p_name', 'p_organization', 'view', 'p_link', 'p_git', 'img', 'p_description',
                  'p_i_did', 'team_link', 'skills']

    def get_team(self, instance):
        request = self.context.get('request')
        link_list = []
        for i in instance.id_teamlist.all():
            teama = {}
            print(i.b_name)
            teama['b_name'] = i.b_name
            teama['b_link'] = i.b_link
            link_list.append(teama)

        return link_list

    def get_image(self, instance):
        request = self.context.get('request')
        webp_list = []
        if type(instance.p_img_large_webp) is dict:
            for i in instance.p_img_large_webp.values():
                my_str = str(i).replace('\\', '/')
                webp_list.append(my_str)
        png_list = []
        if type(instance.p_img_large_png) is dict:
            for i in instance.p_img_large_png.values():
                my_str = str(i).replace('\\', '/')
                png_list.append(my_str)
        img = {}
        img['png'] = png_list
        img['webp'] = webp_list
        return img
