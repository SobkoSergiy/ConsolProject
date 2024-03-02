from django import template
# from .. models import Author, Tag, Quote


register = template.Library()

# @register.filter
# def tags(quote_tags):
#     return ', '.join([str(name) for name in quote_tags.all()])

@register.filter
def get_tags(quote_tags):  # USED in main.html: {% for tag in quote.tags|qtags %}
    qtags = []
    # print("\nquote_tags.all()", quote_tags.all())
    # print("\nquote_tags.all().values()", quote_tags.all().values())
    for name in quote_tags.all(): 
        qtags.append(str(name))
    return qtags

