from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_html_photo')
    # list_display_links = ('id', 'title')
    # search_fields = ('title', 'content')
    # list_editable = ('is_published',)
    # list_filter = ('is_published', 'time_create')
    # prepopulated_fields = {"slug": ('title',)}
    # fields = '__all__'
    fields = (
    'id_category', 'id_view', 'p_organization', 'p_name', 'slug', 'p_description', 'p_i_did', 'p_img', 'p_img_preview_png', 'p_img_preview_webp', 'p_img_large_png', 'p_img_large_webp',
    'get_html_edit', 'p_link', 'skills', 'p_git', 'p_sorting', 'p_status')
    readonly_fields = ('get_html_edit',)

    # save_on_top = True

    def get_html_photo(self, object):
        if object.p_img:
            return mark_safe(f"<img src='{object.p_img.url}' width=60>")

    def get_html_edit(self, object):
        if object.p_img:
            return mark_safe(f"<img src='{object.p_img.url}' width=250>")

    get_html_photo.short_description = 'Миниатюра'

    class Meta:
        model = Project


admin.site.register(Category)
admin.site.register(Project, ProjectAdmin)
admin.site.register(View)
admin.site.register(Skills)
admin.site.register(Team)
admin.site.register(TeamList)
admin.site.register(CatSkill)
