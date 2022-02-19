
menu = [{'title': 'Проекты', 'url': 'home'}, {'title': 'Скиллы', 'url': 'skills'}]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
