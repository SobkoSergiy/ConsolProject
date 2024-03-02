from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from . models import Author, Tag, Quote
from . forms import TagForm , QuoteForm, AuthorForm
# from operator import itemgetter


toptags = [{'t':'_', 'n':'?', 's':'28'}, {'t':'_', 'n':'?', 's':'26'}, {'t':'_', 'n':'?', 's':'24'}, 
           {'t':'_', 'n':'?', 's':'22'}, {'t':'_', 'n':'?', 's':'20'}, {'t':'_', 'n':'?', 's':'18'}, 
           {'t':'_', 'n':'?', 's':'16'}, {'t':'_', 'n':'?', 's':'14'}, {'t':'_', 'n':'?', 's':'12'}, {'t':'_', 'n':'?', 's':'12'}]
cur_page = 1


def get_tagquotes(quotes, tag_name):
    tagquotes = []
    for quote in quotes:            
        for name in quote.tags.all():     
            if tag_name == str(name):
                tagquotes.append(quote)
                break
    return tagquotes


def main_view(request, page=0):
    global cur_page
    quotes = Quote.objects.all()
    if page > 0:
        cur_page = page
    paginator = Paginator(list(quotes), 10, orphans=2) # Show 10 quotes per page.
    page_quotes = paginator.page(cur_page)
    return render(request, "quotes/main.html", context={'quotes': page_quotes, 'toptags': toptags, 'curtag': ''})


def main_view_tag(request, tag_name=''):
    quotes = Quote.objects.all()    # ?? quotes_tags = Quote.objects.values_list('tags')
    if tag_name == '':
        tagquotes = quotes
        tag_head = ''    
    else:    
        get_tag = get_tagquotes(quotes, tag_name)
        tagquotes = quotes if len(get_tag) == 0  else get_tag
        tag_head = f"'{tag_name}' ({len(get_tag)}):"
    return render(request, "quotes/main.html", context={'quotes': tagquotes, 'toptags': toptags, 'curtag': tag_head})


def t10tag(request):
    tags_dict = {}  # {'tag': int, 'tag': int, 'tag': int, ... key: value} 
    quotes = Quote.objects.all()    # ?? quotes_tags = Quote.objects.values_list('tags')
    for quote in quotes:
        for name in quote.tags.all():      
            key = str(name)
            tags_dict[key] = tags_dict[key] + 1  if key in tags_dict.keys() else 1
    # tags_dict = dict(sorted(tags_dict.items(), key=itemgetter(1), reverse=True))  # use itemgetter()
    tags_dict = dict(sorted(tags_dict.items(), key=lambda item: item[1], reverse=True))
    i = 0
    for key, val in tags_dict.items():
        toptags[i]['t'] = f"{key}"
        toptags[i]['n'] = f"{key} ({val})"
        i += 1
        if i > 9:
            break
    return redirect(to='quotes:main')


def author_show(request, author_id):
    author = get_object_or_404(Author, pk=author_id)        
    return render(request, 'quotes/authorshow.html', {"author": author})


@login_required
def tag_change(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})
    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required
def author_change(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            # print("author form is NOT valid !!!   ", form.errors)
            return render(request, 'quotes/author.html', {'form': form})
    return render(request, 'quotes/author.html', {'form': AuthorForm()})


@login_required
def quote_change(request):
    tags = Tag.objects.all().order_by("name")    #.filter(user=request.user)
    auths = Author.objects.all().order_by("fullname")

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, "auths": auths, 'form': form})
    return render(request, 'quotes/quote.html', {"tags": tags, "auths": auths, 'form': QuoteForm()})
    

