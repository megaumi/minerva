# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, ListView
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from reversion.helpers import generate_patch_html
from reversion.revisions import Version
from minerva.main.forms import ArticleForm, TranslatedParagraphForm
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslatedParagraph


class ArticleListView(ListView):
    u'''Список статей заданного выпуска'''
    model = Article
    template_name = "articles_list.html"
    context_object_name = "articles_list"
    def get_queryset(self):
        self.issue = get_object_or_404(MagazineIssue, number__exact=self.kwargs['issue_num'])
        return Article.objects.filter(magazine_issue=self.issue)
    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['issue'] = self.issue
        return context

        
class IssueListView(ListView):
    u'''Список всех выпусков журнала'''
    model = MagazineIssue
    template_name = "issues_list.html"
    context_object_name = "issues_list"

    
def add_article(request):
    u'''Интерфейс для добавления новых статей'''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                translate_article,
                kwargs={'article_id': form.instance.id},
                current_app='minerva.main'
            ))
    else:
        form = ArticleForm()
    context = RequestContext(request, {'form': form})
    return render_to_response('add_article.html', context)


class TranslateArticleView(ListView):
    u'''Страница для работы над статьёй'''
    template_name = 'class_translate_article.html'
    paginate_by = 10
    def get_queryset(self):
        self.article_id = self.kwargs['article_id']
        return EnglishParagraph.objects.filter(article__id=self.article_id)
    def get_context_data(self, **kwargs):
        context = super(TranslateArticleView, self).get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=self.article_id)
        context['title'] = article.original_title
        context['new_translation_form'] = TranslatedParagraphForm()
        return context

class ArticleResultView(ListView):
    u'''Страница с готовым переводом статьи'''
    template_name = 'class_result_article.html'
    def get_queryset(self):
        self.article_id = self.kwargs['article_id']
        return EnglishParagraph.objects.filter(article__id=self.article_id)
    def get_context_data(self, **kwargs):
        context = super(ArticleResultView, self).get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=self.article_id)
        context['article'] = article
        return context

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
        
        
def ajax_get_comments(request, ep_id):
    u'''Отображает список комментариев для абзаца'''
    ep = EnglishParagraph.objects.get(pk=ep_id)
    return render_to_response('comments/comment_list.html', {'ep': ep})
    
    
def get_translation_history(request, translation_id):
    translation = get_object_or_404(TranslatedParagraph, pk=translation_id)
    available_versions = Version.objects.get_for_object(translation)
    history = []
    for i, v in enumerate(available_versions):
        if not i == 0:
            html_patch = generate_patch_html(available_versions[i-1], v, "text")
        else:
            html_patch = v.get_field_dict()['text']
        dataset = {
            'author': User.objects.get(pk=v.get_field_dict()['author']),
            'date': v.get_field_dict()['last_changed'],
            'html_patch': html_patch            
        }
        history.append(dataset)
    return render_to_response('translation_history.html', {'history': history})
    
    
    
#################################################################################
# The below views are currently not in use

def translate_article(request, article_id):
    u'''Страница для работы над статьёй'''
    article = get_object_or_404(Article, pk=article_id)
    english_paragraphs = EnglishParagraph.objects.filter(article__id=article_id)
    paginator = Paginator(english_paragraphs, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        data = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data = paginator.page(paginator.num_pages)
    context = RequestContext(request, {
        'data': data,
        'title': article.original_title,
        'new_translation_form': TranslatedParagraphForm()
    })
    return render_to_response('translate_article.html', context)

# При использовании выдаёт exception NoReverseMatch
class ArticleCreateView(CreateView):
    u'''Интерфейс для добавления новых статей'''
    model = Article
    form_class = ArticleForm
    def get_success_url(self):
        return reverse(
            translate_article,
            kwargs={'article_id': self.object.id},
            current_app='minerva.main'
        )
