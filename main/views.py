# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from minerva.main.forms import ArticleForm, TranslatedParagraphForm
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslatedParagraph

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
    data = []
    for ep in english_paragraphs:
        dataset = {}
        dataset['english_text'] = ep.text
        try:
            dataset['current_translation'] = ep.translation.text
        except TranslatedParagraph.DoesNotExist:
            dataset['current_translation'] = ''
        tp = TranslatedParagraph(
            author=request.user,
            english_paragraph=ep
        )
        dataset['new_translation_form'] = TranslatedParagraphForm(instance=tp)
        data.append(dataset)
    context = {'data': data}
    return render_to_response('translate_article.html', context)
