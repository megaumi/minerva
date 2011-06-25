# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from minerva.main.forms import ArticleForm, TranslatedParagraphForm
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslatedParagraph

class ArticleCreateView(CreateView):
   u'''Интерфейс для добавления новых статей'''
   model = Article
   form_class = ArticleForm
   def get_success_url(self):
       return reverse(translate_article, kwargs={'article_id': self.object.id}, current_app='minerva.main')
      

def add_article(request):
    u'''Интерфейс для добавления новых статей'''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(translate_article, kwargs={'article_id': form.instance.id}, current_app='minerva.main'))
    else:
        form = ArticleForm()
    context = RequestContext(request, {'form': form})
    return render_to_response('add_article.html', context)

def translate_article(request, article_id):
    u'''Страница для работы над статьёй'''
    article = get_object_or_404(Article, pk=article_id)
    english_paragraphs = EnglishParagraph.objects.filter(article__id=article_id)
    data = []
    for ep in english_paragraphs:
        dataset = {
            'ep': ep,
            'new_translation_form': TranslatedParagraphForm()
        }
        data.append(dataset)
    context = RequestContext(request, {'data': data, 'title': article.original_title})
    return render_to_response('translate_article.html', context)

def ajax_add_translation(request, english_paragraph_id):
    u'''Добавляет новый перевод абзаца'''
    ep = EnglishParagraph.objects.get(pk=english_paragraph_id)
    try:
        tp = ep.translation
        if tp.text == request.POST['text']:
            return HttpResponse('Translation not changed')
    except TranslatedParagraph.DoesNotExist:
        tp = TranslatedParagraph(
            author = request.user,
            english_paragraph = ep
        )
    form = TranslatedParagraphForm(request.POST, instance=tp)
    if form.is_valid():
        form.save()
        return HttpResponse('OK')
    else:
        print form.errors.values()
