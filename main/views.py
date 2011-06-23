# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from minerva.main.forms import ArticleForm
from minerva.main.models import MagazineIssue, Article, EnglishParagraph

def add_article(request):
    u'''Интерфейс для добавления новых статей'''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('OK')
    else:
        form = ArticleForm()
    context = RequestContext(request, {'form': form})
    return render_to_response('add_article.html', context)

def translate_article(request, article_id):
    u'''Страница для работы над статьёй'''
    get_object_or_404(Article, pk=article_id)
    english_paragraphs = EnglishParagraph.objects.filter(article__id=article_id)
    context = {'english_paragraphs': english_paragraphs}
    return render_to_response('translate_article.html', context)
