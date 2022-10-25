# about/views.py
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    # Переменная template_name (путь к файлу шаблона)
    # обязательно должна быть объявлена в классе.
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
