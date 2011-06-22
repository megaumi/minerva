# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from minerva.main.forms import ArticleForm
from minerva.main.models import MagazineIssue, Article, EnglishParagraph


def main(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            magazine_issue = form.cleaned_data['magazine_issue']
            original_title = form.cleaned_data['original_title']
            authors = form.cleaned_data['authors']
            url = form.cleaned_data['url']
            text = form.cleaned_data['text']
            article = Article(
                magazine_issue=magazine_issue,
                original_title=original_title,
                authors=authors,
                url=url
            )
            article.save()
            paragraphs = text.split('\n')
            i = 0
            for p in paragraphs:
                if p.strip():
                    ep = EnglishParagraph(article=article, text=p, number=i)
                    ep.save()
                    i += 1
            return HttpResponse('OK')
    else:
        form = ArticleForm()
    rc = RequestContext(request, {'form': form})
    return render_to_response('main.html', rc)
