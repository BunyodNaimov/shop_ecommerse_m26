from django.utils.text import slugify
from unidecode import unidecode

# Транслитерация названия в латиницу
def custom_slugify(text):
    return slugify(unidecode(text))
