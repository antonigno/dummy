from django.http import HttpResponse
from django.template import Context, loader
from search.models import WebSite
from search.forms import SearchForm, AdvancedSearchForm
from search.tables import WebSiteTable
from django.shortcuts import render_to_response, get_object_or_404, render, HttpResponseRedirect, redirect
from django.views.generic.edit import FormView
from django.db.models import Q
from django_tables2   import RequestConfig
import operator

import logging
logger = logging.getLogger('logview.outlog')


def index(request):
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
    if request.session.get('_simple_post'):
        request.POST = request.session.get('_simple_post')
        form = SearchForm(request.POST) # A form bound to the POST data
    elif request.session.get('_advanced_post'):
        request.POST = request.session.get('_advanced_post')
        form = AdvancedSearchForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
        search_words = form.cleaned_data.get('search', '').split()
        all_these_words  = form.cleaned_data.get('all_these_words', '').split()
        this_exact_word_or_phrase = form.cleaned_data.get('this_exact_word_or_phrase', '')
        any_of_these_words = form.cleaned_data.get('any_of_these_words', '').split()
        none_of_these_words = form.cleaned_data.get('none_of_these_words', '').split()
        queries = []
        if search_words:
            for word in search_words:
                q = []
                q.append(Q(**{'body__icontains':word}))
                q.append(Q(**{'title__icontains':word}))
                queries.append(reduce(operator.or_, q))
            qs = WebSite.objects.filter(reduce(operator.and_, queries))
        if all_these_words:
            for word in all_these_words:
                q = []
                q.append(Q(**{'body__icontains':word}))
                q.append(Q(**{'title__icontains':word}))
                queries.append(reduce(operator.or_, q))
            qs = WebSite.objects.filter(reduce(operator.and_, queries))        
        if this_exact_word_or_phrase:
            q = []
            q.append(Q(**{'body__icontains':this_exact_word_or_phrase}))
            q.append(Q(**{'title__icontains':this_exact_word_or_phrase}))
            queries.append(reduce(operator.or_, q))
            qs = WebSite.objects.filter(reduce(operator.and_, queries))
        if any_of_these_words:
            for word in  any_of_these_words:
                q = []
                q.append(Q(**{'body__icontains':word}))
                q.append(Q(**{'title__icontains':word}))
                queries.append(reduce(operator.or_, q))
            qs = WebSite.objects.filter(reduce(operator.or_, queries))
        if none_of_these_words:
            for word in  none_of_these_words:
                q = []
                q.append(~Q(**{'body__icontains':word}))
                q.append(~Q(**{'title__icontains':word}))
                queries.append(reduce(operator.and_, q))
            qs = WebSite.objects.filter(reduce(operator.and_, queries))
        data = []
        for ws in qs:
            data.append({"rank":rank_calc(ws, search_words), "id": ws.id, "url": ws.url, "pub_date": ws.pub_date, "title":ws.title, "body":ws.body} )
        table = WebSiteTable(data)
        RequestConfig(request).configure(table)
        return render(request, 'search/search_results.html', {'table': table, 'form': form})
    else:
        form = SearchForm() # An unbound form
        return render(request, 'search/search_results.html', {
                'form': form,
        })

def search(request):
    if request.method == 'POST': # If the form has been submitted...
        request.session['_simple_post'] = request.POST
        return HttpResponseRedirect('/search_results')
    else:
        form = SearchForm() # An unbound form
    return render(request, 'search/search.html', {
            'form': form,
    })


def advanced_search(request):
    if request.method == 'POST': # If the form has been submitted...
        request.session['_advanced_post'] = request.POST
        return HttpResponseRedirect('/search_results')
    else:
        request.session['_advanced_post'] = None
        request.session['_simple_post'] = None
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
