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
    # # ski = serializers.SerializerMethodField(method_name='get_skills')
    # skils = SkillSerializer(source='skills', many=True)
    # cat = CategorySerializer(source='id_category')
    # team = TeamSerializer(source='id_teamlist', many=True)

    # teams = TeamSerializer(source='team', many=True)

    # categ = CategorySerializer(source='category', many=True)

    id_category = serializers.StringRelatedField(many=False)

    class Meta:
        model = Project
        # depth = 1
        # fields = ['p_name', 'p_description', 'id_category', 'id_teamlist', 'id_view', 'p_organization', 'slug',
        #           'p_i_did',
        #           'p_img', 'png', 'p_img_preview_png', 'p_img_preview_webp', 'p_img_large_png', 'p_img_large_webp',
        #           'p_link', 'skills', 'p_git', 'p_sorting',
        #           'p_status', 'skils', 'cat', 'team']

        fields = ['id', 'id_category', 'p_name', 'p_link', 'png',
                  'webp', 'img']

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

    # def get_skills(self, instance):
    #     request = self.context.get('request')
    #     i = skils
    #     return i


# class ProjectSerializer1(serializers.ModelSerializer):
#     png = serializers.SerializerMethodField(method_name='get_name')
#
#     class Meta:
#         model = Project
#         depth = 1
#         fields = ['p_name', 'p_description', 'id_category', 'id_teamlist', 'id_view', 'p_organization', 'slug',
#                   'p_i_did',
#                   'p_img', 'png', 'p_img_preview_png', 'p_img_preview_webp', 'p_img_large_png', 'p_img_large_webp',
#                   'p_link', 'skills', 'p_git', 'p_sorting',
#                   'p_status']
#
#     def get_name(self, instance):
#         request = self.context.get('request')
#         i = {}
#         i['p_name'] = instance.p_name
#         i['p_description'] = instance.p_description
#         return i

class ProjectDet(serializers.ModelSerializer):
    # skills = serializers.StringRelatedField(many=True)
    # id_category = serializers.StringRelatedField(many=False)
    # id_teamlist = serializers.StringRelatedField(many=True)
    # ski = serializers.SerializerMethodField(method_name='get_skills')
    # skils = SkillSerializer(source='skills', many=True)
    # cat = CategorySerializer(source='id_category')
    # team = TeamSerializer(source='id_teamlist', many=True)

    # teams = TeamSerializer(source='team', many=True)

    # categ = CategorySerializer(source='category', many=True)

    team_link = serializers.SerializerMethodField(method_name='get_name')

    class Meta:
        model = Project
        # fields = ['p_name', 'p_description', 'id_category', 'id_teamlist', 'id_view', 'p_organization', 'slug',
        #           'p_i_did',
        #           'p_img', 'p_img_preview_png', 'p_img_preview_webp', 'p_img_large_png', 'p_img_large_webp',
        #           'p_link', 'skills', 'p_git', 'p_sorting',
        #           'p_status', 'skils', 'cat', 'team']

        fields = ['p_name', 'p_description', 'id_category', 'id_teamlist', 'id_view', 'p_organization', 'slug',
                  'p_i_did',
                  'p_img', 'p_img_preview_png', 'p_img_preview_webp', 'p_img_large_png', 'p_img_large_webp',
                  'p_link', 'skills', 'p_git', 'p_sorting',
                  'p_status', 'team_link']

    def get_name(self, instance):
        request = self.context.get('request')
        link_list = []
        for i in instance.id_teamlist.all():
            link_list.append(i.b_link)
        return link_list
