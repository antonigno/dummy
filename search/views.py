from django.http import HttpResponse
from django.template import Context, loader
from search.models import WebSite
from search.forms import SearchForm, AdvancedSearchForm
from search.tables import WebSiteTable
from django.shortcuts import render_to_response, get_object_or_404, render, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.db.models import Q
from django_tables2   import RequestConfig
import operator

import logging
logger = logging.getLogger('logview.outlog')


def index(request):
#    return HttpResponse("Hello. This is a coding task to show my abilities with python.\
#I used Django framework to realize it.\nAntonino Stefano Borgia")
    site_list = WebSite.objects.all()
    t = loader.get_template('search/index.html')
    c = Context({
        'site_list': site_list,
    })
    return HttpResponse(t.render(c))


def website(request, website_id):
    try:
        w = WebSite.objects.get(pk=website_id)
    except WebSite.DoesNotExist:
        raise Http404
    return render_to_response('search/website.html', {'website': w})
    

def search_results(request):
    return "ciccio"


def search(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            search = form.cleaned_data['search']
            search_words = search.split()
            queries = []
            for word in search_words:
                q = []
                q.append(Q(**{'body__icontains':word}))
                q.append(Q(**{'title__icontains':word}))
                queries.append(reduce(operator.or_, q))
            qs = WebSite.objects.filter(reduce(operator.and_, queries))
            data = []
            for ws in qs:
                data.append({"rank":rank_calc(ws, search_words), "id": ws.id, "url": ws.url, "pub_date": ws.pub_date, "title":ws.title, "body":ws.body} )
            table = WebSiteTable(data)
            RequestConfig(request).configure(table)
            return render(request, 'search/search.html', {'table': table, 'form': form})
    else:
        form = SearchForm() # An unbound form
    return render(request, 'search/search.html', {
        'form': form,
    })


def advanced_search(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AdvancedSearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #search = form.cleaned_data['all_these_words']
            search = form.cleaned_data.get('all_these_words', '')
            search_words = search.split()
            qs = build_query(form)
            # for word in search_words:
            #     q = []
            #     q.append(Q(**{'body__icontains':word}))
            #     q.append(Q(**{'title__icontains':word}))
            #    queries.append(reduce(operator.or_, q))
            #qs = WebSite.objects.filter(reduce(operator.and_, queries))
            data = []
            for ws in qs:
                data.append({"rank":rank_calc(ws, search_words), "id": ws.id, "url": ws.url, "pub_date": ws.pub_date, "title":ws.title, "body":ws.body} )
            table = WebSiteTable(data)
            RequestConfig(request).configure(table)
            return render(request, 'search/advanced_search.html', {'table': table, 'form': form})
    else:
        form = AdvancedSearchForm() # An unbound form
    return render(request, 'search/advanced_search.html', {
        'form': form,
    })


def build_query(form):
    queries = []
    all_these_words = form.cleaned_data.get('all_these_words', '')
    this_exact_word_or_phrase = form.cleaned_data.get('this_exact_word_or_phrase', '')
    any_of_these_words = form.cleaned_data.get('any_of_these_words', '')
    none_of_these_words = form.cleaned_data.get('none_of_these_words', '')
    if all_these_words:
        search_words = all_these_words.split()
        for word in search_words:
            q = []
            q.append(Q(**{'body__icontains':word}))
            q.append(Q(**{'title__icontains':word}))
            queries.append(reduce(operator.or_, q))
    if any_of_these_words:
        search_words = any_of_these_words.split()
        for word in search_words:
            q = []
            q.append(Q(**{'body__icontains':word}))
            q.append(Q(**{'title__icontains':word}))
            queries.append(reduce(operator.or_, q))
    if this_exact_word_or_phrase:
        q = []
        q.append(Q(**{'body__icontains':this_exact_word_or_phrase}))
        q.append(Q(**{'title__icontains':this_exact_word_or_phrase}))
        queries.append(reduce(operator.or_, q))
    if none_of_these_words:
        search_words = none_of_these_words.split()
        for word in search_words:
            q = []
            q.append(~Q(**{'body__icontains':word}))
            q.append(~Q(**{'title__icontains':word}))
            queries.append(reduce(operator.and_, q))
        
    ws = WebSite.objects.filter(reduce(operator.and_, queries))
    logger.error(ws.query)
    return ws

    


def rank_calc(webSite, search_words):
    rank = 0
    for word in search_words:
        r = webSite.meta.filter(keyword=word)
        if r:
            rank += r[0].rank
    return rank


def prova(request):
    rank = [
        {"rank" : 1},
        {"rank" : 2},
        {"rank" : 3},
    ]
    #qs = WebSite.objects.filter(body__icontains="python")
    qs =  WebSite.objects.filter(
        (Q(title__icontains="python") | Q(body__icontains="python")), 
        (Q(body__icontains="hanzo") | Q(title__icontains="hanzo"))
    )
    data = []
    for ws in qs:
        data.append({"id": ws.id, "url": ws.url, "pub_date": ws.pub_date, "title":ws.title, "body":ws.body})
    table = WebSiteTable(data)
    RequestConfig(request).configure(table)
    return render(request, 'search/prova.html', {'table': table})
    #return render(request, 'search/prova.html', {"websites": WebSite.objects.all()})
