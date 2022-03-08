from rest_framework import serializers
from .models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['s_name']


class SkillSerializerfull(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['s_name', 's_description', 's_img', 's_quantity', 's_level']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['c_name']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['b_name']


class CatSkillSerializer(serializers.ModelSerializer):
    skils = SkillSerializerfull(source='skills', many=True)

    class Meta:
        model = CatSkill
        fields = ['cs_name', 'skils']


class ProjectSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField(method_name='get_image')
    id_category = serializers.StringRelatedField(many=False)

    class Meta:
        model = Project
        fields = ['id', 'id_category', 'p_name', 'p_link', 'img']

    def get_image(self, instance):
        request = self.context.get('request')
        webp_list = []
        if type(instance.p_img_large_webp) is dict:
            for i in instance.p_img_large_png.values():
                webp_list.append(i)
        png_list = []
        if type(instance.p_img_large_png) is dict:
            for i in instance.p_img_large_png.values():
                png_list.append(i)
        img = {}
        img['png'] = png_list
        img['webp'] = webp_list
        return img


class ProjectDet(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)
    team_link = serializers.SerializerMethodField(method_name='get_team')
    id_view = serializers.StringRelatedField()
    img = serializers.SerializerMethodField(method_name='get_image')

    class Meta:
        model = Project
        fields = ['p_name', 'p_organization', 'id_view', 'p_link', 'p_git', 'img', 'p_description',
                  'p_i_did', 'team_link', 'skills']

    def get_team(self, instance):
        request = self.context.get('request')
        link_list = []
        teama = {}

        for i in instance.id_teamlist.all():
            print(i.b_name)
            teama['b_name'] = i.b_name
            teama['b_link'] = i.b_link
            print(teama)
            print(link_list)
            link_list.append(teama)
            print(link_list)
        return link_list

    def get_image(self, instance):
        request = self.context.get('request')
        webp_list = []
        if type(instance.p_img_large_webp) is dict:
            for i in instance.p_img_large_png.values():
                webp_list.append(i)
        png_list = []
        if type(instance.p_img_large_png) is dict:
            for i in instance.p_img_large_png.values():
                png_list.append(i)
        img = {}
        img['png'] = png_list
        img['webp'] = webp_list
        return img
